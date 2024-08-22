from __future__ import annotations

from http import HTTPStatus
from typing import Any, Dict, List, Optional, Tuple, Union

import pydantic
from httpx import Response

from .expect import Expect
from .request import RequestService
from .request_config import RequestConfiguration


class Rip:
    """
    The `Rip` class provides a fluent interface for building and configuring the request for an HTTP request.

    """

    def given(self, url: str = "") -> ConfigBuilder:
        """
        Starting point for configuring the request.

        Args:
            url (Optional[str]): The base URL to use for the HTTP requests.

        Returns:
            ConfigBuilder: A new `ConfigBuilder` instance with the specified base URL.
            If no base URL is provided, url configuration must be used.
        """
        return ConfigBuilder(url)


class ConfigBuilder:
    """
    The `ConfigBuilder`class is responsible for building and configuring the request.

    - `url`: Base URL for the HTTP requests.
    - `params`: Query parameters to include in the request.
    - `data`: Request body data (for POST/PUT requests).
    - `json_data`: JSON data to include in the request body.
    - `headers`: HTTP headers to include in the request.
    - `cookies`: Cookies to include in the request.
    - `files`: Files to include in the request.
    - `auth`: Authentication credentials for the request.
    - `proxies`: Proxy configuration for the request.
    - `stream`: Whether to stream the response content.
    - `ssl_verify`: Whether to verify the SSL/TLS certificate of the server.
    - `cert`: Client-side certificate to use for the request.
    - `when`: Returns a `RequestBuilder` instance to execute the request
        The `when()` method returns a `RequestBuilder` instance that can be used
        to execute the HTTP request with the configured.
    """

    def __init__(self, url: str = "") -> None:
        self._request_config = RequestConfiguration(url=url)

    def url(self, url: str) -> ConfigBuilder:
        """
        Sets the base URL for the HTTP requests.

        Args:
            url (str): The URL to use for the HTTP requests.

        Returns:
            ConfigBuilder: The current `ConfigBuilder`instance.
        """
        return self if url is None else self._request_config.update(url=url) or self

    def params(
        self,
        params: Optional[Union[Dict[str, Any], List[tuple], bytes, str]] = None,
    ) -> ConfigBuilder:
        """
        Sets the query parameters for the HTTP requests.

        Args:
            params (Optional[Union[Dict[str, Any], List[tuple], bytes, str]]): The query parameters to use.

        Returns:
            ConfigBuilder: The current `ConfigBuilder`instance.
        """
        return (
            self
            if params is None
            else self._request_config.update(params=params) or self
        )

    def content(
        self, content: Optional[Union[Dict[str, Any], bytes, str]] = None
    ) -> ConfigBuilder:
        """
        Sets the request body in raw bytes/text content for the HTTP requests.

        Args:
            content (Optional[Union[Dict[str, Any], bytes, str]]): The request body to use.

        Returns:
            ConfigBuilder: The current `ConfigBuilder`instance.
        """
        return (
            self
            if content is None
            else self._request_config.update(content=content) or self
        )

    def json(self, json: Optional[Dict[str, Any]] = None) -> ConfigBuilder:
        """
        Sets the JSON data to be included in the request body.

        Args:
            json (Optional[Dict[str, Any]]): The JSON data to include in the request body.

        Returns:
            ConfigBuilder: The current `ConfigBuilder`instance.

        Example:
            json = {"key": "value"}
        """
        return self if json is None else self._request_config.update(json=json) or self

    def headers(self, headers: Optional[Dict[str, Any]] = None) -> ConfigBuilder:
        """
        Sets the headers for the HTTP requests.

        Args:
            headers (Optional[Dict[str, Any]]): The headers to use for the requests.

        Returns:
            ConfigBuilder: The current `ConfigBuilder`instance.
        """
        return (
            self
            if headers is None
            else self._request_config.update(headers=headers) or self
        )

    def cookies(self, cookies: Optional[str] = None) -> ConfigBuilder:
        """
         Sets the cookies for the HTTP requests.

        Args:
            cookies (Optional[str]): The cookies to use for the requests.

        Returns:
            ConfigBuilder: The current `ConfigBuilder`instance.
        """
        return (
            self
            if cookies is None
            else self._request_config.update(cookies=cookies) or self
        )

    def auth(self, auth: Optional[tuple] = None) -> ConfigBuilder:
        """
        Sets the authentication credentials for the HTTP requests.

        Args:
            auth (Optional[Tuple]): The authentication credentials to use.

        Returns:
            ConfigBuilder: The current `ConfigBuilder`instance.
        """
        return self if auth is None else self._request_config.update(auth=auth) or self

    def files(self, files: Optional[Dict[str, Any]] = None) -> ConfigBuilder:
        """
        Sets the files to be uploaded with the HTTP requests.

         Args:
             files (Optional[Dict[str, Any]]): The files to be uploaded.

         Returns:
             ConfigBuilder: The current `ConfigBuilder`instance.
        """
        return (
            self if files is None else self._request_config.update(files=files) or self
        )

    def proxies(self, proxies: Optional[Dict] = None) -> ConfigBuilder:
        """
        Sets the proxy configuration for the HTTP requests.

        Args:
            proxies (Optional[Dict]): The proxy configuration to use.

        Returns:
            ConfigBuilder: The current `ConfigBuilder`instance.
        """
        return (
            self
            if proxies is None
            else self._request_config.update(proxies=proxies) or self
        )

    def stream(self, stream: Optional[bool] = None) -> ConfigBuilder:
        """
        Sets whether to stream the response content.
        if False, the response content will be immediately downloaded.

        Args:
            stream (Optional[bool]): Whether to stream the response content.

        Returns:
            ConfigBuilder: The current `ConfigBuilder`instance.
        """
        return (
            self
            if stream is None
            else self._request_config.update(stream=stream) or self
        )

    def ssl_verify(self, verify: Optional[Union[bool, str]] = None) -> ConfigBuilder:
        """
        Sets the SSL verification setting for the HTTP requests.

        Args:
            verify (Optional[Union[bool, str]]): The SSL verification setting to use.

        Returns:
            ConfigBuilder: The current `ConfigBuilder`instance.
        """
        return (
            self
            if verify is None
            else self._request_config.update(verify=verify) or self
        )

    def cert(self, cert: Optional[Union[str, Tuple[str, str]]] = None) -> ConfigBuilder:
        """
        Sets the SSL certificate to be used in the HTTP requests.

        Args:
            cert (Optional[Cert]): The SSL certificate to use.

        Returns:
            ConfigBuilder: The current `ConfigBuilder`instance.
        """
        return self if cert is None else self._request_config.update(cert=cert) or self

    def when(self) -> RequestBuilder:
        """
        Transitions from the configuration phase to the request building phase.

        Returns:
            RequestBuilder: A new `RequestBuilder` instance configured with the current settings.
        """
        return RequestBuilder(self._request_config)


class RequestBuilder:
    """
    The `RequestBuilder` class is responsible for building and executing HTTP requests.

    - `get`: Sends an HTTP GET request
    - `post`: Sends an HTTP POST request
    - `put`: Sends an HTTP PUT request
    - `patch`: Sends an HTTP PATCH request
    - `delete`: Sends an HTTP DELETE request
    - `options`: Sends an HTTP OPTIONS request
    - `head`: Sends an HTTP HEAD request
    - `trace`: Sends an HTTP TRACE request
    - `connect`: Sends an HTTP CONNECT request
    - `clear`: Clears the request.
    - `copy`: Returns a copy of the `RequestConfig`.
    - `then`: Returns a `ExpectBuilder` to build expectations of HTTP response.
    """

    def __init__(self, request_config: RequestConfiguration) -> None:
        self._request = RequestService()
        self._request_config = request_config

    def _make_request(self, method: str, endpoint: str, **kwargs):
        self._request_config.update(
            url=f"{self._request_config.url}{endpoint}", **kwargs
        )
        self._response = getattr(self._request, method.lower())(
            **self._request_config.parameters
        )
        return self

    def get(self, endpoint: str, **kwargs):
        """
        Sends an HTTP GET request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the GET request to.
            **kwargs: Additional keyword arguments to pass to the the requests.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        return self._make_request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        """
        Sends an HTTP POST request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the POST request to.
            **kwargs: Additional keyword arguments to pass to the the requests.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        return self._make_request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        """
        Sends an HTTP PUT request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the PUT request to.
            **kwargs: Additional keyword arguments to pass to the the requests.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        return self._make_request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        """
        Sends an HTTP DELETE request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the DELETE request to.
            **kwargs: Additional keyword arguments to pass to the the requests.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        return self._make_request("DELETE", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs):
        """
        Sends an HTTP PATCH request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the PATCH request to.
            **kwargs: Additional keyword arguments to pass to the the requests.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        return self._make_request("PATCH", endpoint, **kwargs)

    def head(self, endpoint: str, **kwargs):
        """
        Sends an HTTP HEAD request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the HEAD request to.
            **kwargs: Additional keyword arguments to pass to the the requests.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        return self._make_request("PATCH", endpoint, **kwargs)

    def options(self, endpoint: str, **kwargs):
        """
        Sends an HTTP OPTIONS request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the OPTIONS request to.
            **kwargs: Additional keyword arguments to pass to the the requests.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        return self._make_request("OPTIONS", endpoint, **kwargs)

    def trace(self, endpoint: str, **kwargs):
        """
        Sends an HTTP TRACE request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the TRACE request to.
            **kwargs: Additional keyword arguments to pass to the the requests.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        return self._make_request("TRACE", endpoint, **kwargs)

    def connect(self, endpoint: str, **kwargs):
        """
        Sends an HTTP CONNECT request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the CONNECT request to.
            **kwargs: Additional keyword arguments to pass to the the requests.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        return self._make_request("CONNECT", endpoint, **kwargs)

    def close(self):
        """
        Closes the underlying HTTP session.

        Returns:
            `RequestBuilder`: For building HTTP requests.
        """
        self._request.close()
        return self

    def clear(self):
        """Clears the request parameters defined in the RequestSpecs object."""
        self._request_config.clear()
        return self

    def copy(self):
        """Returns a copy of the current `RequestConfig`."""
        self._request_config.copy()
        return self

    def then(self) -> ExpectBuilder:
        """
        Transitions from the request building phase to the response assertion phase.

        Returns:
            ExpectBuilder: A new `ExpectBuilder` instance for asserting the response.
        """
        return ExpectBuilder(self._response)


class ExpectBuilder:
    def __init__(self, response: Response) -> None:
        self._response = response
        self._expect = Expect(self._response)

    def expect_status(self, status_code: Union[HTTPStatus, int]) -> ExpectBuilder:
        """
        Expect the response to have a specific HTTP status code.

        Args:
            status_code (Union[HTTPStatus, int]): The expected HTTP status code.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self._expect.status(status_code)
        return self

    def expect_headers(self, headers: Dict[str, Any]) -> ExpectBuilder:
        """
        Expect the response to have the specified headers.

        Args:
            headers (Dict[str, Any]): The expected headers to compare against the response headers.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self._expect.headers(headers)
        return self

    def expect_cookies(self, cookies: str) -> ExpectBuilder:
        """
        Expect the response to have the specified cookies.

        Args:
            cookies (str): The expected cookies in the response.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self._expect.cookies(cookies)
        return self

    def expect_header_content_type(self, content_type: Any) -> ExpectBuilder:
        """
        Expect the response's Content-Type header to matches the provided `content_type`.

        Args:
            content_type (Any): The expected Content-Type header value.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self._expect.headers_content_type(content_type)
        return self

    def expect_body(self, text: str) -> ExpectBuilder:
        """
        Expect the content of the response, in unicode, is equal to the expected text.

        Args:
            text (str): The expected text to compare against the response text.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self._expect.body(text)
        return self

    def expect_body_contains(self, value: str) -> ExpectBuilder:
        """
        Expect the response body to contain the specified value.

        Args:
            value (Any): The value that is expected to be contained in the response body.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self._expect.body_contains(value)
        return self

    def expect_json(self, json: Dict[str, Any]) -> ExpectBuilder:
        """
        Expect the response to have the specified JSON body.

        Args:
            json (Dict[str, Any]): The expected JSON body of the response.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self._expect.json(json)
        return self

    def expect_json_contains(self, json: Dict[str, Any]) -> ExpectBuilder:
        """
        Expect the response to contain the specified JSON.

        Args:
            json (Dict[str, Any]): The JSON object that the response to contain.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self._expect.json_contains(json)
        return self

    def expect_key(self, expected_key: str) -> ExpectBuilder:
        """
        Expect the response to have the specified key.

        Args:
            expected_key (str): The key to check for in the response.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self._expect.key(expected_key)
        return self

    def expect_key_value(self, key: str, expected: Any) -> ExpectBuilder:
        """
        Expect the response to have the specified key and value.

        Args:
            key (str): The key to check for in the response.
            expected (Any): The expected value for the specified key.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self._expect.key_value(key, expected)
        return self

    def expect_json_path(self, json_path_expr: str, expected: Any) -> ExpectBuilder:
        """
        Expect the response to have the specified JSON path.

        Args:
            json_path (str): The JSON path to check in the response.
            expected (Any): The expected value at the specified JSON path.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self._expect.json_path(json_path_expr, expected=expected)
        return self

    def expect_json_schema(self, schema: pydantic.BaseModel) -> ExpectBuilder:
        """
        Expect the response to have the specified JSON schema / model.

        Args:
            schema (pydantic.BaseModel): The JSON schema to validate the response against.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self._expect.json_schema(schema)
        return self
