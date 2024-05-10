from __future__ import annotations

from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import pydantic
from requests import Response

from .expect import Expect
from .request import HTTPRequest, RequestService
from .request_config import RequestConfig
from .request_specs import (
    Cert,
    Data,
    QueryParams,
    RequestFiles,
    RequestSpecs,
)


class Rip:
    """
    The `Rip` class provides a fluent interface for building and configuring the request specifications for an HTTP request.
    The `given()` method returns a new instance of the `ConfigBuilder` class, which can be used to configure the request specifications.
    """

    def given(self, base_url: Optional[str] = None) -> ConfigBuilder:
        """
        Constructs a new `ConfigBuilder` instance with the provided base URL.

        Args:
            base_url (Optional[str]): The base URL to use for the HTTP requests.

        Returns:
            ConfigBuilder: A new `ConfigBuilder` instance with the specified base URL.
        """
        return ConfigBuilder(base_url)


class ConfigBuilder:
    """
    The `ConfigBuilder` class is responsible for building and configuring the request specifications
    for an HTTP request. It provides a fluent interface for setting various request configurations.

    - `base_url`: Base URL for the HTTP requests.
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
        to execute the HTTP request with the configured specifications.
    """

    def __init__(self, base_url: Optional[str]) -> None:
        self.__request_specs = RequestSpecs()
        self.__request_config = RequestConfig()
        self.__request_specs.base_url = base_url

    def base_url(self, base_url: str) -> ConfigBuilder:
        """Sets the base URL for the HTTP requests."""
        if base_url is not None:
            self.__request_specs.base_url = base_url
        return self

    def params(self, query_params: Optional[QueryParams] = None) -> ConfigBuilder:
        """
        Sets the request parameters for the HTTP request.

        Example:
            params = {'key1': 'value1', 'key2': 'value2'}
        """
        if query_params is not None:
            self.__request_specs.query_params = query_params
            self.__request_config['params'] = self.__request_specs.query_params
        return self

    def data(self, data: Optional[Data] = None) -> ConfigBuilder:
        """
        Sets the request data for the current request builder.

        Example:
            data = '{"title": "foo", "body": "bar", "userId": 1}'
        """
        if data is not None:
            self.__request_specs.data = data
            self.__request_config['data'] = self.__request_specs.data
        return self

    def json_data(self, json_data: Optional[dict[str, Any]] = None) -> ConfigBuilder:
        """
        Sets the JSON data to be sent in the request body.

        Example:
            json_data = {"key": "value"}
        """
        if json_data is not None:
            self.__request_specs.json_data = json_data
            self.__request_config['json'] = self.__request_specs.json_data
        return self

    def headers(self, headers: Optional[dict[str, Any]] = None) -> ConfigBuilder:
        """
        Sets the headers to be used in the HTTP request.

        Example:
            heaaders = {"Content-type": "application/json; charset=UTF-8"}
        """
        if headers is not None:
            self.__request_specs.headers = headers
            self.__request_config['headers'] = self.__request_specs.headers
        return self

    def cookies(self, cookies: Optional[str] = None) -> ConfigBuilder:
        """
        Sets the cookies to be used in the HTTP request.

        Example:
            cookies = "key1=value1; key2=value2"
        """
        if cookies is not None:
            self.__request_specs.cookies = cookies
            self.__request_config['cookies'] = self.__request_specs.cookies
        return self

    def auth(self, auth: Optional[tuple] = None) -> ConfigBuilder:
        """
        Sets the authentication information for the request.

        Example:
            auth = ('username', 'password')
        """
        if auth is not None:
            self.__request_specs.auth = auth
            self.__request_config['auth'] = self.__request_specs.auth
        return self

    def files(self, files: Optional[RequestFiles] = None) -> ConfigBuilder:
        """
        Sets the files to be sent in the request.

        Example:
            files = {'file': open('report.xls', 'rb')}
        """
        if files is not None:
            self.__request_specs.files = files
            self.__request_config['files'] = self.__request_specs.files
        return self

    def proxies(self, proxies: Optional[dict] = None) -> ConfigBuilder:
        """
        Sets the proxies to be used in the request.

        Example:
            proxies = {'http': 'foo.bar:3128', 'http://host.name': 'foo.bar:4012'}
        """
        if proxies is not None:
            self.__request_specs.proxies = proxies
            self.__request_config['proxies'] = self.__request_specs.proxies
        return self

    def stream(self, stream: Optional[bool] = None) -> ConfigBuilder:
        """
        Sets the stream setting for the request.
        if False, the response content will be immediately downloaded.
        """
        if stream is not None:
            self.__request_specs.stream = stream
            self.__request_config['stream'] = self.__request_specs.stream
        return self

    def ssl_verify(self, verify: Optional[Union[bool, str]] = None) -> ConfigBuilder:
        """
        Sets the SSL verification setting for the request.
        If String, it must be a path to a CA bundle to use.
        """
        if verify is not None:
            self.__request_specs.verify = verify
            self.__request_config['verify'] = self.__request_specs.verify
        return self

    def cert(self, cert: Optional[Cert] = None) -> ConfigBuilder:
        """
        Sets the SSL certificate to be used in the request.
        if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        """
        if cert is not None:
            self.__request_specs.cert = cert
            self.__request_config['cert'] = self.__request_specs.cert
        return self

    def when(self) -> RequestBuilder:
        """
        Returns a `RequestBuilder` instance that can be used to build and execute HTTP requests.

        The `RequestBuilder` instance is configured with the base URL and request specifications from the parent RequestBuilder instance.

        - `get`: Sends an HTTP GET request
        - `post`: Sends an HTTP POST request
        - `put`: Sends an HTTP PUT request
        - `patch`: Sends an HTTP PATCH request
        - `delete`: Sends an HTTP DELETE request
        - `options`: Sends an HTTP OPTIONS request
        - `head`: Sends an HTTP HEAD request
        - `trace`: Sends an HTTP TRACE request
        - `connect`: Sends an HTTP CONNECT request
        - `clear`: Clears the request specifications.
        - `copy`: Returns a copy of the `RequestConfig`.
        - `then`: Returns a `ExpectBuilder` to build expectations of HTTP response.
        """
        request = RequestService(self.__request_specs.base_url)
        return RequestBuilder(request, self.__request_config)


class RequestBuilder:
    def __init__(self, request: HTTPRequest, request_config: RequestConfig) -> None:
        self.__request = request
        self.__request_config = request_config

    def get(self, endpoint: str, **kwargs):
        """
        Sends an HTTP GET request to the specified URL using the request parameters defined in the RequestSpecs object.

        Args:
            endpoint (str): The URL endpoint to send the GET request to.
            kwargs (dict[str, Any]): Additional keyword arguments to pass to the underlying requests library.

        Returns:
            `RequestBuilder`: For building expectations of HTTP response.
        """
        self.__request_config.update(**kwargs) or None
        self.__response = self.__request.get(
            endpoint, **self.__request_config.parameters
        )
        return self

    def post(
        self,
        endpoint: str,
        **kwargs,
    ):
        """
        Sends an HTTP POST request to the specified URL using the request parameters defined in the RequestSpecs object.

        Args:
            endpoint (str): The endpoint to send the POST request to.
            kwargs (dict[str, Any]): Additional keyword arguments to pass to the underlying requests library.

        Returns:
            `RequestBuilder`: For building expectations of HTTP response.
        """
        self.__request_config.update(**kwargs) or None
        self.__response = self.__request.post(
            endpoint, **self.__request_config.parameters
        )
        return self

    def put(self, endpoint: str, **kwargs):
        """
        Sends an HTTP PUT request to the specified URL using the request parameters defined in the RequestSpecs object.

        Args:
            endpoint (str): The URL endpoint to send the PUT request to.
            kwargs (dict[str, Any]): Additional keyword arguments to pass to the underlying requests library.

        Returns:
            `RequestBuilder`: For building expectations of HTTP response.
        """
        self.__request_config.update(**kwargs) or None
        self.__response = self.__request.put(
            endpoint, **self.__request_config.parameters
        )
        return self

    def delete(self, endpoint: str, **kwargs: dict[str, Any]) -> RequestBuilder:
        """
        Sends an HTTP DELETE request to the specified URL using the request parameters defined in the RequestSpecs object.

        Args:
            endpoint (str): The URL endpoint to send the DELETE request to.
            kwargs (dict[str, Any]): Additional keyword arguments to pass to the underlying requests library.

        Returns:
            `RequestBuilder`: For building expectations of HTTP response.
        """
        self.__request_config.update(**kwargs) or None
        self.__response = self.__request.delete(
            endpoint, **self.__request_config.parameters
        )
        return self

    def patch(self, endpoint: str, **kwargs) -> RequestBuilder:
        """
        Sends an HTTP PATCH request to the specified URL using the request parameters defined in the RequestSpecs object.

        Args:
            endpoint (str): The URL endpoint to send the PATCH request to.
            kwargs (dict[str, Any]): Additional keyword arguments to pass to the underlying requests library.

        Returns:
            `RequestBuilder`: For building expectations of HTTP response.
        """
        self.__request_config.update(**kwargs) or None
        self.__response = self.__request.patch(
            endpoint, **self.__request_config.parameters
        )
        return self

    def head(self, endpoint: str, **kwargs) -> RequestBuilder:
        """
        Sends an HTTP HEAD request to the specified URL using the request parameters defined in the RequestSpecs object.

        Args:
            endpoint (str): The URL endpoint to send the HEAD request to.
            kwargs (dict[str, Any]): Additional keyword arguments to pass to the underlying requests library.

        Returns:
            `RequestBuilder`: For building expectations of HTTP response.
        """
        self.__request_config.update(**kwargs) or None
        self.__response = self.__request.head(
            endpoint, **self.__request_config.parameters
        )
        return self

    def options(self, endpoint: str, **kwargs) -> RequestBuilder:
        """
        Sends an HTTP OPTIONS request to the specified URL using the request parameters defined in the RequestSpecs object.

        Args:
            endpoint (str): The URL endpoint to send the request to.
            kwargs (dict[str, Any]): Additional keyword arguments to pass to the underlying requests library.

        Returns:
            `RequestBuilder`: For building expectations of HTTP response.
        """
        self.__request_config.update(**kwargs) or None
        self.__response = self.__request.options(
            endpoint, **self.__request_config.parameters
        )
        return self

    def trace(self, endpoint: str, **kwargs) -> RequestBuilder:
        """
        Sends an HTTP TRACE request to the specified URL using the request parameters defined in the RequestSpecs object.

        Args:
            endpoint (str): The URL endpoint to send the TRACE request to.
            kwargs (dict[str, Any]): Additional keyword arguments to pass to the underlying requests library.

        Returns:
            `RequestBuilder`: For building expectations of HTTP response.
        """
        self.__request_config.update(**kwargs) or None
        self.__response = self.__request.trace(
            endpoint, **self.__request_config.parameters
        )
        return self

    def connect(self, endpoint: str, **kwargs) -> RequestBuilder:
        """
        Sends an HTTP CONNECT request to the specified URL using the request parameters defined in the RequestSpecs object.

        Args:
            endpoint (str): The URL endpoint to send the CONNECT request to.
            kwargs (dict[str, Any]): Additional keyword arguments to pass to the underlying requests library.

        Returns:
            `RequestBuilder`: For building expectations of HTTP response.
        """
        self.__request_config.update(**kwargs) or None
        self.__response = self.__request.connect(
            endpoint, **self.__request_config.parameters
        )
        return self

    def close(self) -> RequestBuilder:
        """
        Closes the underlying HTTP session.

        Returns:
            `RequestBuilder`: For building HTTP requests.
        """
        self.__request.close()
        return self

    def clear(self) -> RequestBuilder:
        """Clears the request parameters defined in the RequestSpecs object."""
        self.__request_config.clear()
        return self

    def copy(self) -> RequestBuilder:
        """Returns a copy of the current `RequestConfig`."""
        self.__request_config.copy()
        return self

    def then(self) -> ExpectBuilder:
        """
        Returns a `ExpectBuilder` instance that can be used to build expectations for the response of an HTTP request.

        It provides a fluent interface for defining various expectations, such as:
        - Expecting a specific HTTP status code
        - Expecting a specific Content-Type header
        - Expecting specific headers
        - Expecting specific cookies
        - Expecting the response body to match certain criteria (e.g. equal to, contain, be valid JSON, etc.)

        The `ExpectBuilder` is typically used in conjunction with the `RequestBuilder` class, which is responsible
        for building the HTTP request. The `ExpectBuilder` is returned by the `then(), allowing for chaining of expectations.
        """
        return ExpectBuilder(self.__response)


class ExpectBuilder:
    def __init__(self, response: Response) -> None:
        self.__response = response
        self.__expect = Expect(self.__response)

    def expect_status(self, status_code: Union[HTTPStatus, int]) -> ExpectBuilder:
        """
        Expect the response to have a specific HTTP status code.

        Args:
            status_code (Union[HTTPStatus, int]): The expected HTTP status code.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self.__expect.status(status_code)
        return self

    def expect_headers(self, headers: Dict[str, Any]) -> ExpectBuilder:
        """
        Expect the response to have the specified headers.

        Args:
            headers (Dict[str, Any]): The expected headers to compare against the response headers.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self.__expect.headers(headers)
        return self

    def expect_cookies(self, cookies: str) -> ExpectBuilder:
        """
        Expect the response to have the specified cookies.

        Args:
            cookies (str): The expected cookies in the response.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self.__expect.cookies(cookies)
        return self

    def expect_header_content_type(self, content_type: Any) -> ExpectBuilder:
        """
        Expect the response's Content-Type header to matches the provided `content_type`.

        Args:
            content_type (Any): The expected Content-Type header value.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self.__expect.headers_content_type(content_type)
        return self

    def expect_body(self, text: str) -> ExpectBuilder:
        """
        Expect the content of the response, in unicode, is equal to the expected text.

        Args:
            text (str): The expected text to compare against the response text.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self.__expect.body(text)
        return self

    def expect_body_contains(self, value: str) -> ExpectBuilder:
        """
        Expect the response body to contain the specified value.

        Args:
            value (Any): The value that is expected to be contained in the response body.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self.__expect.body_contains(value)
        return self

    def expect_json(self, json: Dict[str, Any]) -> ExpectBuilder:
        """
        Expect the response to have the specified JSON body.

        Args:
            json (Dict[str, Any]): The expected JSON body of the response.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self.__expect.json(json)
        return self

    def expect_json_contains(self, json: Dict[str, Any]) -> ExpectBuilder:
        """
        Expect the response to contain the specified JSON.

        Args:
            json (Dict[str, Any]): The JSON object that the response to contain.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self.__expect.json_contains(json)
        return self

    def expect_key(self, expected_key: str) -> ExpectBuilder:
        """
        Expect the response to have the specified key.

        Args:
            expected_key (str): The key to check for in the response.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self.__expect.key(expected_key)
        return self

    def expect_key_value(self, key: str, expected_value: Any) -> ExpectBuilder:
        """
        Expect the response to have the specified key and value.

        Args:
            key (str): The key to check for in the response.
            expected_value (Any): The expected value for the specified key.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self.__expect.key_value(key, expected_value)
        return self

    def expect_json_path(
        self, json_path_expr: str, expected_value: Any
    ) -> ExpectBuilder:
        """
        Expect the response to have the specified JSON path.

        Args:
            json_path (str): The JSON path to check in the response.
            expected_value (Any): The expected value at the specified JSON path.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self.__expect.json_path(json_path_expr, expected_value)
        return self

    def expect_json_schema(self, schema: pydantic.BaseModel) -> ExpectBuilder:
        """
        Expect the response to have the specified JSON schema / model.

        Args:
            schema (pydantic.BaseModel): The JSON schema to validate the response against.

        Returns:
            ExpectBuilder: The current `ExpectBuilder` instance, for chaining additional expectations.
        """
        self.__expect.json_schema(schema)
        return self
