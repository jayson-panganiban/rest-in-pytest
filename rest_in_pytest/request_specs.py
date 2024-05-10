from __future__ import annotations

from typing import IO, Any, Optional, Tuple, Union

# types
QueryParams = Union[dict[str, Any], list[tuple], bytes, str]
Data = Union[dict[str, Any], bytes, str]
RequestFiles = Union[dict[str, IO[Any]]]
Cert = Union[str, Tuple[str, str]]


class RequestSpecs:
    """
    Represents the specifications for an HTTP request, including the base URL, parameters, data, headers, cookies, files, authentication, and other options.

    This class provides a convenient way to manage and configure the various aspects of an HTTP request, making it easier to work with the requests library in a structured and organized manner.

    Attributes:
        `base_url`: The base URL for the request.
        `query_params`: The query parameters for the request.
        `data`: The request body data.
        `headers`: The request headers.
        `cookies`: The request cookies.
        `verify`: Whether to verify the SSL/TLS certificate of the remote host.
        `auth`: The authentication credentials for the request.
        `files`: The files to be uploaded with the request.
        `proxies`: The proxy configuration for the request.
        `stream`: Whether to stream the response content.
        `cert`: The path to an SSL/TLS certificate or a tuple of (cert, key) file paths.
        `json_data`: The JSON data to be included in the request body.
    """

    def __init__(self) -> None:
        self._base_url = None
        self._query_params = None
        self._data = None
        self._headers = None
        self._cookies = None
        self._files = None
        self._auth = None
        # TODO: NotImplemented
        # self._timout = None,
        # self._allow_redirects=True,
        # self.hooks=None,
        self._stream = None
        self._proxies = None
        self._verify = None
        self._cert = None
        self._json_data = None

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, url) -> None:
        self._base_url = url

    @property
    def query_params(self) -> Optional[QueryParams]:
        return self._query_params

    @query_params.setter
    def query_params(self, query_params) -> None:
        self._query_params = query_params

    @property
    def data(self) -> Optional[Data]:
        return self._data

    @data.setter
    def data(self, data) -> None:
        self._data = data

    @property
    def headers(self) -> Optional[dict[str, Any]]:
        return self._headers

    @headers.setter
    def headers(self, headers) -> None:
        self._headers = headers

    @property
    def cookies(self) -> Optional[str]:
        return self._cookies

    @cookies.setter
    def cookies(self, cookies) -> None:
        self._cookies = cookies

    @property
    def verify(self) -> Optional[Union[bool, str]]:
        return self._verify

    @verify.setter
    def verify(self, verify) -> None:
        self._verify = verify

    @property
    def auth(self) -> Optional[tuple]:
        return self._auth

    @auth.setter
    def auth(self, auth) -> None:
        self._auth = auth

    @property
    def files(self) -> Optional[RequestFiles]:
        return self._files

    @files.setter
    def files(self, files) -> None:
        self._files = files

    @property
    def proxies(self) -> Optional[dict]:
        return self._proxies

    @proxies.setter
    def proxies(self, proxies) -> None:
        self._proxies = proxies

    @property
    def stream(self) -> Optional[bool]:
        return self._stream

    @stream.setter
    def stream(self, stream):
        self._stream = stream

    @property
    def cert(self) -> Optional[Cert]:
        return self._cert

    @cert.setter
    def cert(self, cert):
        self._cert = cert

    @property
    def json_data(self) -> Optional[dict[str, Any]]:
        return self._json_data

    @json_data.setter
    def json_data(self, json_data):
        self._json_data = json_data
