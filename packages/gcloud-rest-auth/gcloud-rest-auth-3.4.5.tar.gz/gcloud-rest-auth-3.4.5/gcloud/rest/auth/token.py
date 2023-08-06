"""
Google Cloud auth via service account file
"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from builtins import int
from builtins import open
from builtins import str
from builtins import object
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
import datetime
import enum
import json
import os
import time
from typing import Any
from typing import AnyStr
from typing import Dict
from typing import IO
from typing import List
from typing import Optional
from typing import Union
from six.moves.urllib.parse import urlencode

import backoff
import cryptography  # pylint: disable=unused-import
import jwt

from .build_constants import BUILD_GCLOUD_REST
from .session import SyncSession
# N.B. the cryptography library is required when calling jwt.encrypt() with
# algorithm='RS256'. It does not need to be imported here, but this allows us
# to throw this error at load time rather than lazily during normal operations,
# where plumbing this error through will require several changes to otherwise-
# good error handling.

# Handle differences in exceptions
try:
    # TODO: Type[Exception] should work here, no?
    CustomFileError      = FileNotFoundError
except NameError:
    CustomFileError = IOError


# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Response
    from requests import Session
else:
    from aiohttp import ClientResponse as Response  # type: ignore[no-redef]
    from aiohttp import ClientSession as Session  # type: ignore[no-redef]
    import asyncio

GCE_METADATA_BASE = 'http://metadata.google.internal/computeMetadata/v1'
GCE_METADATA_HEADERS = {'metadata-flavor': 'Google'}
GCE_ENDPOINT_PROJECT = ('{}/project/project-id'.format((GCE_METADATA_BASE)))
GCE_ENDPOINT_TOKEN = ('{}/instance/service-accounts'
                      '/default/token?recursive=true'.format((GCE_METADATA_BASE)))
GCLOUD_TOKEN_DURATION = 3600
REFRESH_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}


class Type(enum.Enum):
    AUTHORIZED_USER = 'authorized_user'
    GCE_METADATA = 'gce_metadata'
    SERVICE_ACCOUNT = 'service_account'


def get_service_data(
        service                                  )                  :
    service = service or os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if not service:
        cloudsdk_config = os.environ.get('CLOUDSDK_CONFIG')
        sdkpath = (cloudsdk_config
                   or os.path.join(os.path.expanduser('~'), '.config',
                                   'gcloud'))
        service = os.path.join(sdkpath, 'application_default_credentials.json')
        set_explicitly = bool(cloudsdk_config)
    else:
        set_explicitly = True

    try:
        try:
            with open(service) as f:  # type: ignore[arg-type]
                data                 = json.loads(f.read())
                return data
        except TypeError:
            data = json.loads(service.read())  # type: ignore[union-attr]
            return data
    except CustomFileError:
        if set_explicitly:
            # only warn users if they have explicitly set the service_file path
            raise

        return {}
    except Exception:  # pylint: disable=broad-except
        return {}


class Token(object):
    # pylint: disable=too-many-instance-attributes
    def __init__(self, service_file                                   = None,
                 session                    = None,
                 scopes                      = None)        :
        self.service_data = get_service_data(service_file)
        if self.service_data:
            self.token_type = Type(self.service_data['type'])
            self.token_uri = self.service_data.get(
                'token_uri', 'https://oauth2.googleapis.com/token')
        else:
            # At this point, all we can do is assume we're running somewhere
            # with default credentials, eg. GCE.
            self.token_type = Type.GCE_METADATA
            self.token_uri = GCE_ENDPOINT_TOKEN

        self.session = SyncSession(session)
        self.scopes = ' '.join(scopes or [])
        if self.token_type == Type.SERVICE_ACCOUNT and not self.scopes:
            raise Exception('scopes must be provided when token type is '
                            'service account')

        self.access_token                = None
        self.access_token_duration = 0
        self.access_token_acquired_at = datetime.datetime(1970, 1, 1)

        self.acquiring                                = None  # pylint: disable=unsubscriptable-object,line-too-long

    def get_project(self)                 :
        project = (os.environ.get('GOOGLE_CLOUD_PROJECT')
                   or os.environ.get('GCLOUD_PROJECT')
                   or os.environ.get('APPLICATION_ID'))

        if self.token_type == Type.GCE_METADATA:
            self.ensure_token()
            resp = self.session.get(GCE_ENDPOINT_PROJECT, timeout=10,
                                          headers=GCE_METADATA_HEADERS)

            if not project:
                try:
                    project = resp.text()
                except (AttributeError, TypeError):
                    project = str(resp.text)

        elif self.token_type == Type.SERVICE_ACCOUNT:
            project = project or self.service_data.get('project_id')

        return project

    def get(self)                 :
        self.ensure_token()
        return self.access_token

    def ensure_token(self)        :
        if self.acquiring:
            self.acquiring
            return

        if not self.access_token:
            self.acquiring = (self.acquire_access_token())
            self.acquiring
            return

        now = datetime.datetime.utcnow()
        delta = (now - self.access_token_acquired_at).total_seconds()
        if delta <= self.access_token_duration / 2:
            return

        self.acquiring = (self.acquire_access_token())
        self.acquiring

    def _refresh_authorized_user(self, timeout     )            :
        payload = urlencode({
            'grant_type': 'refresh_token',
            'client_id': self.service_data['client_id'],
            'client_secret': self.service_data['client_secret'],
            'refresh_token': self.service_data['refresh_token'],
        })

        data           = self.session.post(url=self.token_uri,
                                                 data=payload,
                                                 headers=REFRESH_HEADERS,
                                                 timeout=timeout)
        return data

    def _refresh_gce_metadata(self, timeout     )            :
        resp           = self.session.get(url=self.token_uri,
                                                headers=GCE_METADATA_HEADERS,
                                                timeout=timeout)
        return resp

    def _refresh_service_account(self, timeout     )            :
        now = int(time.time())
        assertion_payload = {
            'aud': self.token_uri,
            'exp': now + GCLOUD_TOKEN_DURATION,
            'iat': now,
            'iss': self.service_data['client_email'],
            'scope': self.scopes,
        }

        # N.B. algorithm='RS256' requires an extra 240MB in dependencies...
        assertion = jwt.encode(assertion_payload,
                               self.service_data['private_key'],
                               algorithm='RS256')
        payload = urlencode({
            'assertion': assertion,
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        })

        resp           = self.session.post(self.token_uri, data=payload,
                                                 headers=REFRESH_HEADERS,
                                                 timeout=timeout)
        return resp

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)  # type: ignore
    def acquire_access_token(self, timeout      = 10)        :
        if self.token_type == Type.AUTHORIZED_USER:
            resp = self._refresh_authorized_user(timeout=timeout)
        elif self.token_type == Type.GCE_METADATA:
            resp = self._refresh_gce_metadata(timeout=timeout)
        elif self.token_type == Type.SERVICE_ACCOUNT:
            resp = self._refresh_service_account(timeout=timeout)
        else:
            raise Exception('unsupported token type {}'.format((self.token_type)))

        content = resp.json()

        self.access_token = str(content['access_token'])
        self.access_token_duration = int(content['expires_in'])
        self.access_token_acquired_at = datetime.datetime.utcnow()
        self.acquiring = None

    def close(self)        :
        self.session.close()

    def __enter__(self)           :
        return self

    def __exit__(self, *args     )        :
        self.close()
