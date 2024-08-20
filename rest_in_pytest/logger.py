from __future__ import annotations

import logging
from functools import lru_cache
from typing import Final
from http.client import HTTPConnection


class Logger:
    DEBUG_LEVEL: Final[int] = 1

    def __init__(self, name: str = __name__) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._setup_logger()

    def _setup_logger(self) -> None:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)


@lru_cache(maxsize=None)
def get_logger(name: str = __name__) -> Logger:
    return Logger(name)


HTTPConnection.debuglevel = Logger.DEBUG_LEVEL

logger = get_logger()
