from __future__ import annotations

from http import HTTPStatus
from typing import Any, Dict, Union

import jsonpath
import pydantic
from assertpy import assert_that
from httpx import Response

from .logger import logger


from functools import wraps


def log_assertion(description):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            logger.info(f"Asserting {description}")
            if func.__name__ == "json_path":
                expected = args[1] if len(args) > 1 else kwargs.get("expected")
            else:
                expected = args[0] if args else kwargs.get("expected")
            logger.info(f"Expected: {expected}")
            actual = func(self, *args, **kwargs)
            logger.info(f"Actual: {actual}")
            return self

        return wrapper

    return decorator


class Expect:
    def __init__(self, response: Response) -> None:
        self._response = response

    @log_assertion("status code")
    def status(self, status_code: Union[HTTPStatus, int]) -> int:
        assert_that(status_code).is_equal_to(self._response.status_code)
        return self._response.status_code

    @log_assertion("successful status code")
    def status_success(self) -> int:
        assert_that(self._response.is_success).is_true()
        return self._response.status_code

    @log_assertion("headers")
    def headers(self, headers: Dict[str, Any]) -> Dict[str, Any]:
        assert_that(headers).is_equal_to(dict(self._response.headers))
        return dict(self._response.headers)

    @log_assertion("Content-Type header")
    def headers_content_type(self, content_type: str) -> Any:
        actual_content_type = self._response.headers.get("Content-Type")
        assert_that(content_type).is_equal_to(actual_content_type)
        return actual_content_type

    @log_assertion("cookies")
    def cookies(self, cookies: str) -> str:
        assert_that(cookies).is_equal_to(str(self._response.cookies))
        return str(self._response.cookies)

    @log_assertion("content")
    def content(self, content: Any) -> bytes:
        assert_that(content).is_equal_to(self._response.content)
        return self._response.content

    @log_assertion("body text")
    def body(self, text: str) -> str:
        assert_that(text).is_equal_to(self._response.text)
        return self._response.text

    @log_assertion("body contains")
    def body_contains(self, value: Any) -> str:
        assert_that(self._response.text).contains(value)
        return self._response.text

    @log_assertion("JSON contains key")
    def key(self, key: str) -> Any:
        assert_that(self._response.json()).contains_key(key)
        return self._response.json()

    @log_assertion("JSON key-value pair")
    def key_value(self, key: str, value: Any) -> Any:
        assert_that(self._response.json()).contains_key_value(key, value)
        return self._response.json().get(key)

    @log_assertion("JSON equality")
    def json(self, json: Dict[str, Any]) -> Any:
        response_json = self._response.json()
        assert_that(json).is_equal_to(response_json)
        return response_json

    @log_assertion("JSON contains")
    def json_contains(self, json: Dict[str, Any]) -> Any:
        assert_that(self._response.json()).contains(json)
        return self._response.json()

    @log_assertion("JSON path")
    def json_path(self, json_path_expr: str, expected: str) -> Any:
        """A query language for JSON, allowing to extract specific parts of JSON"""
        matches = jsonpath.findall(json_path_expr, self._response.json())
        assert_that(expected).is_equal_to(matches)
        return matches

    @log_assertion("JSON schema")
    def json_schema(self, schema: Union[pydantic.BaseModel, Dict[str, Any]]) -> Any:
        response_json = self._response.json()
        assert_that(response_json).is_equal_to(schema)
        return response_json
