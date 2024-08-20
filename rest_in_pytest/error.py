from __future__ import annotations

from typing import Any

from .logger import logger


class Base(Exception):
    """Base class for all errors"""

    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message)
        self.message = message
        self.__dict__.update(kwargs)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"


class Error(Base):
    """Represents an error that occurred during a request."""


class HTTPError(Error):
    """Represents an HTTP error with status code."""

    def __init__(self, message: str, status_code: int, **kwargs: Any) -> None:
        super().__init__(message, status_code=status_code, **kwargs)
        logger.error(f"HTTP Error {status_code}: {message}")


class ValidationError(Error):
    """Represents a validation error."""


class TimeoutError(Error):
    """Represents a timeout error."""


class ConnectionError(Error):
    """Represents a connection error."""
