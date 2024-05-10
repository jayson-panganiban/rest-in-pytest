from __future__ import annotations

from http import HTTPStatus
from typing import Any, Dict, List, Union

import jsonpath
import pydantic
from assertpy import assert_that
from requests import Response


class Expect:
    def __init__(self, response: Response) -> None:
        self._response = response

    def status(self, status_code: Union[HTTPStatus, int]) -> None:
        assert_that(status_code).is_equal_to(self._response.status_code)

    def status_ok(self) -> None:
        """Asserts that the response is successful (status code 200-299)."""
        assert_that(self._response.ok).is_true()

    def headers(self, headers: Dict[str, Any]) -> None:
        assert_that(headers).is_equal_to(self._response.headers)

    def headers_content_type(self, content_type: str) -> None:
        assert_that(content_type).is_equal_to(self._response.headers['Content-Type'])

    def cookies(self, cookies: str) -> None:
        assert_that(cookies).is_equal_to(self._response.cookies)

    def content(self, content: Any) -> None:
        """Represens the raw binary data of the response body. It can be a text, JSON, images, etc"""
        assert_that(content).is_equal_to(self._response.content)

    def body(self, text: str) -> None:
        """Represents the decoded textual representation of the HTTP response body."""
        assert_that(text).is_equal_to(self._response.text)

    def body_contains(self, value: Any) -> None:
        assert_that(self._response.text).contains(value)

    def key(self, key: str) -> None:
        assert_that(self._response.json()).contains_key(key)

    def key_value(self, key: str, value: Any) -> None:
        assert_that(self._response.json()).contains_key_value(key, value)

    def json(self, json: Dict[str, Any]) -> None:
        """Represents data formatted as JSON, convertible to dict or list"""
        assert_that(json).is_equal_to(self._response.json())

    def json_contains(self, json: Dict[str, Any]) -> None:
        assert_that(self._response.json()).contains(json)

    def json_path(self, json_path_expr: str, expected_value: str) -> None:
        """A query language for JSON, allowing to extract specific parts of JSON using path expressions"""
        json_path_matches = self._json_path_matches(json_path_expr)
        for match in json_path_matches:
            assert_that(match.value).is_equal_to(expected_value)

    def json_schema(self, schema: Union[pydantic.BaseModel, Dict[str, Any]]) -> None:
        """A vocabulary that allows to annotate and validate JSON documents"""
        assert_that(schema).is_equal_to(self._response.json())

    def _json_path_matches(self, json_path_expr: str) -> List[JsonPathMatch]:
        if not json_path_expr:
            return []
        matches = jsonpath.findall(json_path_expr, self._response.json())
        return [JsonPathMatch(value) for value in matches]


class JsonPathMatch:
    def __init__(self, value: Any):
        self.value = value
