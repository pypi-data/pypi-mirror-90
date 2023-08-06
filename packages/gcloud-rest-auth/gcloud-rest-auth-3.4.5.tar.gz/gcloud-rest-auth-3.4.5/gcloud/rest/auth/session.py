from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from builtins import object
import logging
import threading
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from typing import Any
from typing import Dict
from typing import IO
from typing import Optional

from .build_constants import BUILD_GCLOUD_REST

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Response
    from requests import Session
else:
    from aiohttp import ClientResponse as Response  # type: ignore[no-redef]
    from aiohttp import ClientSession as Session  # type: ignore[no-redef]


log = logging.getLogger(__name__)


class BaseSession(object):
    __metaclass__ = ABCMeta

    def __init__(self, session                    = None, timeout      = 10,
                 verify_ssl       = True)        :
        self._session = session
        self._ssl = verify_ssl
        self._timeout = timeout

    @abstractproperty
    def session(self)                     :
        return self._session

    @abstractmethod
    def post(self, url     , headers                ,
                   data               , timeout     ,
                   params                          )            :
        pass

    @abstractmethod
    def get(self, url     , headers                          ,
                  timeout     , params                          )            :
        pass

    @abstractmethod
    def put(self, url     , headers                , data         ,
                  timeout     )            :
        pass

    @abstractmethod
    def delete(self, url     , headers                ,
                     params                , timeout     )            :
        pass

    @abstractmethod
    def request(self, method     , url     , headers                ,
                      auto_raise_for_status       = True,
                      **kwargs     )            :
        pass

    @abstractmethod
    def close(self)        :
        pass


if not BUILD_GCLOUD_REST:
    import aiohttp

    def _raise_for_status(resp                        )        :
        """Check resp for status and if error log additional info."""
        # Copied from aiohttp's raise_for_status() -- since it releases the
        # response payload, we need to grab the `resp.text` first to help users
        # debug.
        #
        # Useability/performance notes:
        # * grabbing the response can be slow for large files, only do it as
        #   needed
        # * we can't know in advance what encoding the files might have unless
        #   we're certain in advance that the result is an error payload from
        #   Google (otherwise, it could be a binary blob from GCS, for example)
        # * sometimes, errors are expected, so we should try to avoid polluting
        #   logs in that case
        #
        # https://github.com/aio-libs/aiohttp/blob/
        # 385b03ef21415d062886e1caab74eb5b93fdb887/aiohttp/
        # client_reqrep.py#L892-L902
        if resp.status >= 400:
            assert resp.reason is not None
            # Google's error messages are useful, pass 'em through
            body = resp.text(errors='replace')
            resp.release()
            raise aiohttp.ClientResponseError(resp.request_info, resp.history,
                                              status=resp.status,
                                              message='{}: {}'.format((resp.reason), (body)),
                                              headers=resp.headers)

    class AioSession(BaseSession):
        @property
        def session(self)                         :
            connector = aiohttp.TCPConnector(ssl=self._ssl)
            self._session = self._session or aiohttp.ClientSession(
                connector=connector, timeout=self._timeout)
            return self._session

        def post(self, url     , headers                ,
                       data                = None, timeout      = 10,
                       params                           = None
                       )                          :
            resp = self.session.post(url, data=data, headers=headers,
                                           timeout=timeout, params=params)
            _raise_for_status(resp)
            return resp

        def get(self, url     , headers                           = None,
                      timeout      = 10,
                      params                           = None
                      )                          :
            resp = self.session.get(url, headers=headers,
                                          timeout=timeout, params=params)
            _raise_for_status(resp)
            return resp

        def put(self, url     , headers                , data         ,
                      timeout      = 10)                          :
            resp = self.session.put(url, data=data, headers=headers,
                                          timeout=timeout)
            _raise_for_status(resp)
            return resp

        def delete(self, url     , headers                ,
                         params                           = None,
                         timeout      = 10
                         )                          :
            resp = self.session.delete(url, headers=headers,
                                             params=params, timeout=timeout)
            _raise_for_status(resp)
            return resp

        def request(self, method     , url     , headers                ,
                          auto_raise_for_status       = True, **kwargs     
                          )                          :
            resp = self.session.request(method, url, headers=headers,
                                              **kwargs)
            if auto_raise_for_status:
                _raise_for_status(resp)
            return resp

        def close(self)        :
            if self._session:
                self._session.close()  # type: ignore[func-returns-value]


if BUILD_GCLOUD_REST:
    class SyncSession(BaseSession):
        _google_api_lock = threading.RLock()

        @property
        def google_api_lock(self)                   :
            return SyncSession._google_api_lock  # pylint: disable=protected-access

        @property
        def session(self)           :
            self._session = self._session or Session()
            self._session.verify = self._ssl
            return self._session

        # N.B.: none of these will be `async` in compiled form, but adding the
        # symbol ensures we match the base class's definition for static
        # analysis.
        def post(self, url     , headers                ,
                       data                = None, timeout      = 10,
                       params                           = None)            :
            with self.google_api_lock:
                resp = self.session.post(url, data=data, headers=headers,
                                         timeout=timeout, params=params)
            resp.raise_for_status()
            return resp

        def get(self, url     , headers                           = None,
                      timeout      = 10,
                      params                           = None)            :
            with self.google_api_lock:
                resp = self.session.get(url, headers=headers, timeout=timeout,
                                        params=params)
            resp.raise_for_status()
            return resp

        def put(self, url     , headers                , data         ,
                      timeout      = 10)            :
            with self.google_api_lock:
                resp = self.session.put(url, data=data, headers=headers,
                                        timeout=timeout)
            resp.raise_for_status()
            return resp

        def delete(self, url     , headers                ,
                         params                           = None,
                         timeout      = 10
                         )            :
            with self.google_api_lock:
                resp = self.session.delete(url, params=params, headers=headers,
                                           timeout=timeout)
            resp.raise_for_status()
            return resp

        def request(self, method     , url     , headers                ,
                          auto_raise_for_status       = True, **kwargs     
                          )            :
            with self.google_api_lock:
                resp = self.session.request(method, url, headers=headers,
                                            **kwargs)
            if auto_raise_for_status:
                resp.raise_for_status()
            return resp

        def close(self)        :
            if self._session:
                self._session.close()
