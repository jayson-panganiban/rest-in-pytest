from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union, IO


@dataclass
class RequestConfiguration:
    """
    Represents the HTTP request configuration, including the url, params, data, headers, cookies, and other options.

    Attributes:
        `url`: The target URL for the request.
        `params`: The query parameters for the request.
        `data`: The request body in raw bytes/text content.
        `headers`: The request headers.
        `cookies`: The request cookies.
        `files`: The files to be uploaded with the request.
        `auth`: The authentication credentials for the request.
        `stream`: Whether to stream the response content.
        `proxies`: The proxy configuration for the request.
        `verify`: Whether to verify the SSL/TLS certificate of the remote host.
        `cert`: The path to an SSL/TLS certificate or a tuple of (cert, key) file paths.
        `json`: The JSON data to be included in the request body.
    """

    url: str = ""
    params: Optional[Union[Dict[str, Any], List[Tuple], bytes, str]] = None
    content: Optional[Union[Dict[str, Any], bytes, str]] = None
    headers: Optional[Dict[str, Any]] = None
    cookies: Optional[str] = None
    files: Optional[Dict[str, IO[Any]]] = None
    auth: Optional[Tuple] = None
    stream: Optional[bool] = None
    proxies: Optional[Dict] = None
    verify: Optional[Union[bool, str]] = None
    cert: Optional[Union[str, Tuple[str, str]]] = None
    json: Optional[Dict[str, Any]] = None
    parameters: Dict[str, Any] = field(default_factory=dict)

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if not isinstance(k, str):
                raise ValueError(f"Key {k} must be a string")
            if v is not None and not isinstance(v, (str, int, float, dict, list)):
                raise ValueError(
                    f"Value for key {k} must be a string, number, dict, or list"
                )
            setattr(self, k, v)
            self.parameters[k] = v

    def clear(self):
        for attr in self.__annotations__:
            if attr != "url":
                setattr(self, attr, None)
        self.parameters.clear()

    def copy(self):
        return RequestConfiguration(
            **{attr: getattr(self, attr) for attr in self.__annotations__}
        )
