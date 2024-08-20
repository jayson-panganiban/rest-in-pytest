from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class RequestConfig:
    """
    Represents a request configuration for a REST API request.

    The `RequestConfig` class provides a way to manage the parameters for a REST API request, such as headers, query parameters, and request body.
    It allows you to update the parameters in a convenient way, and provides an iterator to access the parameters.
    """

    parameters: Dict[str, Any] = field(default_factory=dict)

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if not isinstance(k, str):
                raise ValueError(f"Key {k} must be a string")
            if v is not None and not isinstance(v, (str, int, float, dict, list)):
                raise ValueError(
                    f"Key {k} must be a string and value must be a string, number or dict"
                )
            self.parameters[k] = v

    def clear(self):
        self.parameters.clear()

    def copy(self):
        return RequestConfig(self.parameters.copy())
