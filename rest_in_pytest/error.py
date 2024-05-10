from __future__ import annotations


class Base(Exception):
    """Base class for all of the errors"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self._message = message

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.message}'


class Error(Base):
    """Represents an error that occurred during a request."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
