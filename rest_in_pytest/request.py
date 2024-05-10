from __future__ import annotations

import json
from http import HTTPMethod
from typing import Any, Protocol
from urllib.parse import urljoin

import requests
from requests.exceptions import RequestException

from .error import Error
from .logger import logger


class HTTPRequest(Protocol):
    def get(self, endpoint: str, **kwargs) -> requests.Response: ...
    def post(self, endpoint: str, **kwargs) -> requests.Response: ...
    def put(self, endpoint: str, **kwargs) -> requests.Response: ...
    def delete(self, endpoint: str, **kwargs) -> requests.Response: ...
    def patch(self, endpoint: str, **kwargs) -> requests.Response: ...
    def head(self, endpoint: str, **kwargs) -> requests.Response: ...
    def options(self, endpoint: str, **kwargs) -> requests.Response: ...
    def connect(self, endpoint: str, **kwargs) -> requests.Response: ...
    def trace(self, endpoint: str, **kwargs) -> requests.Response: ...
    def close(self) -> None: ...


class RequestService:
    def __init__(self, base_url) -> None:
        self._base_url = base_url
        self._session = requests.Session()

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request(method=HTTPMethod.GET, endpoint=endpoint, **kwargs)

    def post(
        self,
        endpoint: str,
        **kwargs,
    ) -> requests.Response:
        return self._request(method=HTTPMethod.POST, endpoint=endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        return self._request(method=HTTPMethod.PUT, endpoint=endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._request(method=HTTPMethod.DELETE, endpoint=endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs):
        return self._request(method=HTTPMethod.PATCH, endpoint=endpoint, **kwargs)

    def head(self, endpoint: str, **kwargs):
        return self._request(method=HTTPMethod.HEAD, endpoint=endpoint, **kwargs)

    def options(self, endpoint: str, **kwargs):
        return self._request(method=HTTPMethod.OPTIONS, endpoint=endpoint, **kwargs)

    def connect(self, endpoint: str, **kwargs):
        return self._request(method=HTTPMethod.CONNECT, endpoint=endpoint, **kwargs)

    def trace(self, endpoint: str, **kwargs):
        return self._request(method=HTTPMethod.TRACE, endpoint=endpoint, **kwargs)

    def close(self):
        self._session.close()

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = urljoin(self._base_url, endpoint)
        logger.info(f'Request: {method} {url} \nkwargs: {kwargs}')
        try:
            response = self._session.request(method=method, url=url, **kwargs)
            if not self._status_code_is_success(response):
                logger.debug(
                    f'Response text: {response.text}, Status code: {response.status_code}'
                )
            return response
        except RequestException as e:
            raise Error(f'Request Error: {e}')

    def _handle_data(self, **kwargs) -> dict[str, Any]:
        # At least one argument must be provided
        if all(key in kwargs for key in ('data', 'json')):
            raise ValueError(
                "At least one of 'data' or 'json' arguments must be provided"
            )
        if 'data' in kwargs:
            # Serialize 'data' to a JSON formatted str.
            if isinstance(kwargs['data'], dict):
                kwargs['data'] = json.dumps(kwargs['data'])
        return kwargs

    def _status_code_is_success(self, response: requests.Response) -> bool:
        return 200 <= response.status_code <= 299
