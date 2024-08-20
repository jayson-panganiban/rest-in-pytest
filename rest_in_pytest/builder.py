from __future__ import annotations

from http import HTTPStatus
from typing import Any, Dict, List, Optional, Tuple, Union

import pydantic
from httpx import Response

from .expect import Expect
from .request import RequestService
from .request_config import RequestConfig
from .request_specs import RequestSpecs


class Rip:
    """
    The `Rip` class provides a fluent interface for building and configuring the request specifications for an HTTP request.
    The `given()` method returns a new instance of the `ConfigBuilder` class, which can be used to configure the request specifications.
    """

    def given(self, base_url: str = "") -> ConfigBuilder:
        """
        Constructs a new `ConfigBuilder` instance with the provided base URL. If no base URL is provided, base_url configuration must be used.

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

    def __init__(self, base_url: str = "") -> None:
        self._request_specs = RequestSpecs()
        self._request_config = RequestConfig()
        self._request_specs.base_url = base_url

    def base_url(self, base_url: str) -> ConfigBuilder:
        """
        Sets the base URL for the HTTP requests.

        Args:
            base_url (str): The base URL to use for the HTTP requests.

        Returns:
            ConfigBuilder: The current `ConfigBuilder` instance.
        """
        if base_url is not None:
            self._request_specs.base_url = base_url
        return self

    def query_params(
        self,
        query_params: Optional[Union[Dict[str, Any], List[tuple], bytes, str]] = None,
    ) -> ConfigBuilder:
        """
        Sets the query parameters for the HTTP requests.

        Args:
            query_params (Optional[Union[Dict[str, Any], List[tuple], bytes, str]]): The query parameters to use.

        Returns:
            ConfigBuilder: The current `ConfigBuilder` instance.
        """
        if query_params is not None:
            self._request_specs.query_params = query_params
            self._request_config.parameters["params"] = query_params
        return self

    def data(
        self, data: Optional[Union[Dict[str, Any], bytes, str]] = None
    ) -> ConfigBuilder:
        """
        Sets the request body data for the HTTP requests.

        Args:
            data (Optional[Union[Dict[str, Any], bytes, str]]): The request body data to use.

        Returns:
            ConfigBuilder: The current `ConfigBuilder` instance.
        """
        if data is not None:
            self._request_specs.data = data
            self._request_config.parameters["data"] = data
        return self

    def json_data(self, json_data: Optional[Dict[str, Any]] = None) -> ConfigBuilder:
        """
        Sets the JSON data to be included in the request body.

        Args:
            json_data (Optional[Dict[str, Any]]): The JSON data to include in the request body.

        Returns:
            ConfigBuilder: The current `ConfigBuilder` instance.

        Example:
            json_data = {"key": "value"}
        """
        if json_data is not None:
            self._request_specs.json_data = json_data
            self._request_config.parameters["json"] = json_data
        return self

    def headers(self, headers: Optional[Dict[str, Any]] = None) -> ConfigBuilder:
        """
        Sets the headers for the HTTP requests.

        Args:
            headers (Optional[Dict[str, Any]]): The headers to use for the requests.

        Returns:
            ConfigBuilder: The current `ConfigBuilder` instance.
        """
        if headers is not None:
            self._request_specs.headers = headers
            self._request_config.parameters["headers"] = headers
        return self

    def cookies(self, cookies: Optional[str] = None) -> ConfigBuilder:
        """
         Sets the cookies for the HTTP requests.

        Args:
            cookies (Optional[str]): The cookies to use for the requests.

        Returns:
            ConfigBuilder: The current `ConfigBuilder` instance.
        """
        if cookies is not None:
            self._request_specs.cookies = cookies
            self._request_config.parameters["cookies"] = cookies
        return self

    def auth(self, auth: Optional[tuple] = None) -> ConfigBuilder:
        """
        Sets the authentication credentials for the HTTP requests.

        Args:
            auth (Optional[Tuple]): The authentication credentials to use.

        Returns:
            ConfigBuilder: The current `ConfigBuilder` instance.
        """
        if auth is not None:
            self._request_specs.auth = auth
            self._request_config.parameters["auth"] = auth
        return self

    def files(self, files: Optional[Dict[str, Any]] = None) -> ConfigBuilder:
        """
        Sets the files to be uploaded with the HTTP requests.

         Args:
             files (Optional[Dict[str, Any]]): The files to be uploaded.

         Returns:
             ConfigBuilder: The current `ConfigBuilder` instance.
        """
        if files is not None:
            self._request_specs.files = files
            self._request_config.parameters["files"] = files
        return self

    def proxies(self, proxies: Optional[Dict] = None) -> ConfigBuilder:
        """
        Sets the proxy configuration for the HTTP requests.

        Args:
            proxies (Optional[Dict]): The proxy configuration to use.

        Returns:
            ConfigBuilder: The current `ConfigBuilder` instance.
        """
        if proxies is not None:
            self._request_specs.proxies = proxies
            self._request_config.parameters["proxies"] = proxies
        return self

    def stream(self, stream: Optional[bool] = None) -> ConfigBuilder:
        """
        Sets whether to stream the response content.
        if False, the response content will be immediately downloaded.

        Args:
            stream (Optional[bool]): Whether to stream the response content.

        Returns:
            ConfigBuilder: The current `ConfigBuilder` instance.
        """
        if stream is not None:
            self._request_specs.stream = stream
            self._request_config.parameters["stream"] = stream
        return self

    def ssl_verify(self, verify: Optional[Union[bool, str]] = None) -> ConfigBuilder:
        """
        Sets the SSL verification setting for the HTTP requests.

        Args:
            verify (Optional[Union[bool, str]]): The SSL verification setting to use.

        Returns:
            ConfigBuilder: The current `ConfigBuilder` instance.
        """
        if verify is not None:
            self._request_specs.verify = verify
            self._request_config.parameters["verify"] = verify
        return self

    def cert(self, cert: Optional[Union[str, Tuple[str, str]]] = None) -> ConfigBuilder:
        """
        Sets the SSL certificate to be used in the HTTP requests.

        Args:
            cert (Optional[Cert]): The SSL certificate to use.

        Returns:
            ConfigBuilder: The current `ConfigBuilder` instance.
        """
        if cert is not None:
            self._request_specs.cert = cert
            self._request_config.parameters["cert"] = cert
        return self

    def when(self) -> RequestBuilder:
        """
        Transitions from the configuration phase to the request building phase.
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

        Returns:
            RequestBuilder: A new `RequestBuilder` instance configured with the current settings.
        """
        if self._request_specs.base_url is None:
            raise ValueError("Base URL must be set before making a request")
        return RequestBuilder(
            RequestService(self._request_specs.base_url), self._request_config
        )


class RequestBuilder:
    def __init__(self, request: RequestService, request_config: RequestConfig) -> None:
        """
        Initializes a new `RequestBuilder` instance.

        Args:
            request (RequestService): The `RequestService` instance to use for making HTTP requests.
            request_config (RequestConfig): The `RequestConfig` instance containing the request configuration.
        """
        self._request = request
        self._request_config = request_config

    def get(self, endpoint: str, **kwargs):
        """
        Sends an HTTP GET request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the GET request to.
            **kwargs: Additional keyword arguments to pass to the underlying requests library.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        self._request_config.update(**kwargs)
        self._response = self._request.get(endpoint, **self._request_config.parameters)
        return self

    def post(self, endpoint: str, **kwargs):
        """
        Sends an HTTP POST request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the POST request to.
            **kwargs: Additional keyword arguments to pass to the underlying requests library.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        self._request_config.update(**kwargs)
        self._response = self._request.post(endpoint, **self._request_config.parameters)
        return self

    def put(self, endpoint: str, **kwargs):
        """
        Sends an HTTP PUT request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the PUT request to.
            **kwargs: Additional keyword arguments to pass to the underlying requests library.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        self._request_config.update(**kwargs)
        self._response = self._request.put(endpoint, **self._request_config.parameters)
        return self

    def delete(self, endpoint: str, **kwargs):
        """
        Sends an HTTP DELETE request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the DELETE request to.
            **kwargs: Additional keyword arguments to pass to the underlying requests library.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        self._request_config.update(**kwargs)
        self._response = self._request.delete(
            endpoint, **self._request_config.parameters
        )
        return self

    def patch(self, endpoint: str, **kwargs):
        """
        Sends an HTTP PATCH request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the PATCH request to.
            **kwargs: Additional keyword arguments to pass to the underlying requests library.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        self._request_config.update(**kwargs)
        self._response = self._request.patch(
            endpoint, **self._request_config.parameters
        )
        return self

    def head(self, endpoint: str, **kwargs):
        """
        Sends an HTTP HEAD request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the HEAD request to.
            **kwargs: Additional keyword arguments to pass to the underlying requests library.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        self._request_config.update(**kwargs)
        self._response = self._request.head(endpoint, **self._request_config.parameters)
        return self

    def options(self, endpoint: str, **kwargs):
        """
        Sends an HTTP OPTIONS request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the OPTIONS request to.
            **kwargs: Additional keyword arguments to pass to the underlying requests library.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        self._request_config.update(**kwargs)
        self._response = self._request.options(
            endpoint, **self._request_config.parameters
        )
        return self

    def trace(self, endpoint: str, **kwargs):
        """
        Sends an HTTP TRACE request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the TRACE request to.
            **kwargs: Additional keyword arguments to pass to the underlying requests library.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        self._request_config.update(**kwargs)
        self._response = self._request.trace(
            endpoint, **self._request_config.parameters
        )
        return self

    def connect(self, endpoint: str, **kwargs):
        """
        Sends an HTTP CONNECT request to the specified endpoint.

        Args:
            endpoint (str): The URL endpoint to send the CONNECT request to.
            **kwargs: Additional keyword arguments to pass to the underlying requests library.

        Returns:
            RequestBuilder: The current `RequestBuilder` instance.
        """
        self._request_config.update(**kwargs)
        self._response = self._request.connect(
            endpoint, **self._request_config.parameters
        )
        return self

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

        It provides a fluent interface for defining various expectations, such as:
        - Expecting a specific HTTP status code
        - Expecting a specific Content-Type header
        - Expecting specific headers
        - Expecting specific cookies
        - Expecting the response body to match certain criteria (e.g. equal to, contain, be valid JSON, etc.)
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
