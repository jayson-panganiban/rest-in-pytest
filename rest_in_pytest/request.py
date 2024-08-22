from __future__ import annotations

import json
from http import HTTPMethod
from typing import Any

import httpx
from httpx import Response
from .error import ConnectionError, HTTPError, TimeoutError
from .logger import logger


class RequestService:
    def __init__(self) -> None:
        self._client = httpx.Client()

    def get(self, **kwargs) -> Response:
        return self._request(method=HTTPMethod.GET, **kwargs)

    def post(self, **kwargs) -> Response:
        return self._request(method=HTTPMethod.POST, **kwargs)

    def put(self, **kwargs) -> Response:
        return self._request(method=HTTPMethod.PUT, **kwargs)

    def delete(self, **kwargs) -> Response:
        return self._request(method=HTTPMethod.DELETE, **kwargs)

    def patch(self, **kwargs) -> Response:
        return self._request(method=HTTPMethod.PATCH, **kwargs)

    def head(self, **kwargs) -> Response:
        return self._request(method=HTTPMethod.HEAD, **kwargs)

    def options(self, **kwargs) -> Response:
        return self._request(method=HTTPMethod.OPTIONS, **kwargs)

    def connect(self, **kwargs) -> Response:
        return self._request(method=HTTPMethod.CONNECT, **kwargs)

    def trace(self, **kwargs) -> Response:
        return self._request(method=HTTPMethod.TRACE, **kwargs)

    def close(self) -> None:
        self._client.close()

    def _request(self, method: str, **kwargs) -> Response:
        headers = kwargs.get("headers", {})
        logger.info(f"Request headers: {headers}")

        if "content" in kwargs:
            logger.info(f"Request content: {kwargs['content']}")
        if "json" in kwargs:
            logger.info(f"Request JSON: {kwargs['json']}")

        try:
            response = self._client.request(method=method, **kwargs)

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
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

    def _handle_data(self, **kwargs) -> dict[str, Any]:
        # At least one argument must be provided
        if all(key in kwargs for key in ("content", "json")):
            raise ValueError(
                "Only one of 'content' or 'json' arguments can be provided"
            )
        if "content" in kwargs and isinstance(kwargs["content"], dict):
            kwargs["content"] = json.dumps(kwargs["content"])
        return kwargs

    @staticmethod
    def _status_code_is_success(response: Response) -> bool:
        return 200 <= response.status_code < 300
