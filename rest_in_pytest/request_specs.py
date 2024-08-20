from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple, Union, Any, IO


@dataclass
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
        `files`: The files to be uploaded with the request.
        `auth`: The authentication credentials for the request.
        `stream`: Whether to stream the response content.
        `proxies`: The proxy configuration for the request.
        `verify`: Whether to verify the SSL/TLS certificate of the remote host.
        `cert`: The path to an SSL/TLS certificate or a tuple of (cert, key) file paths.
        `json_data`: The JSON data to be included in the request body.
    """

    base_url: str = ""
    query_params: Optional[Union[Dict[str, Any], List[Tuple], bytes, str]] = None
    data: Optional[Union[Dict[str, Any], bytes, str]] = None
    headers: Optional[Dict[str, Any]] = None
    cookies: Optional[str] = None
    files: Optional[Dict[str, IO[Any]]] = None
    auth: Optional[Tuple] = None
    stream: Optional[bool] = None
    proxies: Optional[Dict] = None
    verify: Optional[Union[bool, str]] = None
    cert: Optional[Union[str, Tuple[str, str]]] = None
    json_data: Optional[Dict[str, Any]] = None
