from __future__ import annotations

from typing import Any, Iterator, Optional, Union


class RequestConfig:
    """
    Represents a request configuration for a REST API request.

    The `RequestConfig` class provides a way to manage the parameters for a REST API request, such as headers, query parameters, and request body.
    It allows you to update the parameters in a convenient way, and provides an iterator to access the parameters.
    """

    def __init__(self) -> None:
        self.parameters: dict[str, Any] = {}

    def __str__(self) -> str:
        return f'RequestConfig with parameters: {self.parameters}'

    def __repr__(self) -> str:
        return f'RequestConfig({vars(self)})'

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        return iter(vars(self).items())

    def __getitem__(self, key: str) -> Any:
        return self.parameters[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.parameters[key] = value

    def update(
        self,
        **kwargs: Optional[
            Union[dict[str, Any], bytes, str, tuple[Any, ...], bool, list[Any]]
        ],
    ):
        """
        Updates the parameters of the RequestConfig object with the provided keyword arguments.

        Args:
            **kwargs: Optional dictionary, bytes, string, tuple, boolean, or list values to update the parameters with.

        Raises:
            ValueError: If any of the keys in the kwargs are not strings, or if any of the values are not strings, numbers, or dictionaries.
        """
        for k, v in kwargs.items():
            if not isinstance(k, str):
                raise ValueError(f'Key {k} must be a string')
            if v is not None and not isinstance(v, (str, int, float, dict, list)):
                raise ValueError(
                    f'Key {k} must be a string and value must be a string, number or dict'
                )

            self.parameters[k] = v

    def clear(self) -> None:
        self.parameters.clear()

    def copy(self) -> 'RequestConfig':
        new_config = RequestConfig()
        new_config.parameters.update(self.parameters)
        return new_config
