import time
from json import JSONDecodeError
from typing import Callable
from loguru import logger

import requests

from microclient.utils import truncate_if_necessary

REPR_LIMIT = 50

JSON_CONTENT = 'application/json'


class LazyResponse:

    def __init__(self, method_call: Callable[..., requests.Response], url: str, method: str, data=None, headers=None):
        self._response: requests.Response = None
        self._response_loaded = False
        self._get_response = method_call
        self.url = url
        self.method = method
        self.request_data = data
        self.response_time = None
        self.request_headers = headers

    def _truncate_long_strings(self):
        method = truncate_if_necessary(self.method, REPR_LIMIT)
        request_data = truncate_if_necessary(self.request_data, REPR_LIMIT)
        request_headers = truncate_if_necessary(self.request_headers, REPR_LIMIT)
        return method, request_data, request_headers

    def _load_response(self):
        if not self._response_loaded:
            method, request_data, request_headers = self._truncate_long_strings()
            logger.info(f"REQUEST: {self.url} | method: {method} | data: {request_data} | headers: {request_headers}")
            start = time.time()
            self._response = self._get_response()
            self.response_time = time.time() - start
            self._response_loaded = True
            logger.info(f"RESPONSE: {self.url} | {self.status} | {self.response_time:.4f} seconds")

    @property
    def data(self):
        self._load_response()
        content_type = self._response.headers['Content-Type']
        if JSON_CONTENT in content_type:
            try:
                response_data = self._response.json()
            except JSONDecodeError:
                logger.warning(f"{self.url} did not respond with valid JSON, falling back to raw content (probably HTML).")
                response_data = self._response.content
        else:
            # TODO for now, every other content type is falling back to raw data
            response_data = self._response.content
        return response_data

    @property
    def status(self):
        self._load_response()
        return self._response.status_code

    @property
    def headers(self):
        self._load_response()
        return self._response.headers

    def __repr__(self):
        method, request_data, _ = self._truncate_long_strings()
        return f"LazyResponse(request_data={request_data}, url={self.url}, method={method})"

    def __str__(self):
        return str(self.data)
