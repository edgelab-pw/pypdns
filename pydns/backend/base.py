__author__ = 'Vinzenz Stadtmueller'
__copyright__ = '(c) Edgelab e.U. 2016'
__licence__ = 'Apache 2.0'

from requests import Request, Session
import os
import json
import posixpath
import logging

# Python 3 compatibility:
try:
    import httplib
except ImportError:  # py3
    from http import client as httplib
try:
    import urlparse
except ImportError:  # py3
    from urllib import parse as urlparse
try:
    basestring
except NameError:  # py3
    basestring = (bytes, str)

logger = logging.getLogger(__name__)


class PyPdnsResourceBase(object):
    def __getattr__(self, item):
        if item.startswith("_"):
            raise AttributeError(item)

        kwargs = self._store.copy()
        kwargs['base_url'] = self.url_join(self._store["base_url"], item)

        return PyPdnsResource(**kwargs)

    def url_join(self, base, *args):
        scheme, netloc, path, query, fragment = urlparse.urlsplit(base)
        path = path if len(path) else "/"
        path = posixpath.join(path, *[('%s' % x) for x in args])
        return urlparse.urlunsplit([scheme, netloc, path, query, fragment])


class ResourceException(Exception):
    pass


class PyPdnsResource(PyPdnsResourceBase):
    def __init__(self, **kwargs):
        self._store = kwargs

    def __call__(self, resource_id=None):
        if not resource_id:
            return self

        if isinstance(resource_id, basestring):
            resource_id = resource_id.split("/")
        elif not isinstance(resource_id, (tuple, list)):
            resource_id = [str(resource_id)]

        kwargs = self._store.copy()
        if resource_id is not None:
            kwargs["base_url"] = self.url_join(self._store["base_url"], *resource_id)

        return self.__class__(**kwargs)

    def _request(self, method, data=None, params=None):
        url = self._store["base_url"]
        if data:
            logger.info('%s %s %r', method, url, data)
        else:
            logger.info('%s %s', method, url)

        s = Session()

        req = Request(method, url, data=data, headers=self._store["api_key"], params=params)
        prepped = req.prepare()

        resp = s.send(prepped)

        logger.debug('Status code: %s, output: %s', resp.status_code, resp.content)

        if resp.status_code >= 400:
            raise ResourceException("{0} {1}".format(resp.status_code, httplib.responses[resp.status_code]))
        elif 200 <= resp.status_code <= 299:
            return self._store["serializer"].loads(resp)

    def get(self, *args, **params):
        return self(args)._request("GET", params=params)

    def post(self, *args, **data):
        return self(args)._request("POST", data=data)

    def put(self, *args, **data):
        return self(args)._request("PUT", data=data)

    def delete(self, *args, **params):
        return self(args)._request("DELETE", params=params)

    def create(self, *args, **data):
        return self.post(*args, **data)

    def set(self, *args, **data):
        return self.put(*args, **data)


class JsonSerializer(object):
    content_types = [
        "application/json",
        "application/x-javascript",
        "text/javascript",
        "text/x-javascript",
        "text/x-json"
    ]

    def get_accept_types(self):
        return ", ".join(self.content_types)

    def loads(self, response):
        try:
            return json.loads(response.content.decode('utf-8'))
        except (UnicodeDecodeError, ValueError):
            return response.content


class PyPdnsResourceAPI(PyPdnsResourceBase):
    def __init__(self, host, apikey):
        self._store = {
            "base_url": host,
            "api_key": {'X-API-Key': apikey},
            "serializer": JsonSerializer(),
        }
