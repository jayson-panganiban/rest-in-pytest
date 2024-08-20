from __future__ import annotations

import json
from http import HTTPMethod
from typing import Any
from urllib.parse import urljoin

import httpx
from httpx import Response
from urllib.parse import urlencode
from .error import ConnectionError, HTTPError, TimeoutError
from .logger import logger


class RequestService:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._client = httpx.Client()

    def get(self, endpoint: str, **kwargs) -> Response:
        return self._request(method=HTTPMethod.GET, endpoint=endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Response:
        return self._request(method=HTTPMethod.POST, endpoint=endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Response:
        return self._request(method=HTTPMethod.PUT, endpoint=endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response:
        return self._request(method=HTTPMethod.DELETE, endpoint=endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Response:
        return self._request(method=HTTPMethod.PATCH, endpoint=endpoint, **kwargs)

    def head(self, endpoint: str, **kwargs) -> Response:
        return self._request(method=HTTPMethod.HEAD, endpoint=endpoint, **kwargs)

    def options(self, endpoint: str, **kwargs) -> Response:
        return self._request(method=HTTPMethod.OPTIONS, endpoint=endpoint, **kwargs)

    def connect(self, endpoint: str, **kwargs) -> Response:
        return self._request(method=HTTPMethod.CONNECT, endpoint=endpoint, **kwargs)

    def trace(self, endpoint: str, **kwargs) -> Response:
        return self._request(method=HTTPMethod.TRACE, endpoint=endpoint, **kwargs)

    def close(self) -> None:
        self._client.close()

    def _request(self, method: str, endpoint: str, **kwargs) -> Response:
        url = urljoin(self._base_url, endpoint)

        # Log the full URL including query parameters
        full_url = (
            f"{url}?{urlencode(kwargs.get('params', {}))}"
            if kwargs.get("params")
            else url
        )
        logger.info(f"Sending {method} request to {full_url}")

        # Log headers
        headers = kwargs.get("headers", {})
        logger.info(f"Request headers: {headers}")

        # Log other request data
        if "data" in kwargs:
            logger.info(f"Request data: {kwargs['data']}")
        if "json" in kwargs:
            logger.info(f"Request JSON: {kwargs['json']}")

        try:
            response = self._client.request(method=method, url=url, **kwargs)
            logger.debug(f"Response received: Status {response.status_code}")

            if not self._status_code_is_success(response):
                logger.debug(
                    f"Response text: {response.text}, Status code: {response.status_code}"
                )
                raise HTTPError(
                    f"HTTP Error {response.status_code}",
                    status_code=response.status_code,
                    response=response,
                )
            return response
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}")
        except httpx.NetworkError as e:
            raise ConnectionError(f"Network error occurred: {e}")

    def _handle_data(self, **kwargs) -> dict[str, Any]:
        # At least one argument must be provided
        if all(key in kwargs for key in ("data", "json")):
            raise ValueError("Only one of 'data' or 'json' arguments can be provided")
        if "data" in kwargs and isinstance(kwargs["data"], dict):
            kwargs["data"] = json.dumps(kwargs["data"])
        return kwargs

    @staticmethod
    def _status_code_is_success(response: Response) -> bool:
        return 200 <= response.status_code < 300
