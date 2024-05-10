from __future__ import annotations

import logging
from http.client import HTTPConnection
from typing import Optional

HTTPConnection.debuglevel = 1


class Logger:
    """This class ensures that there is only one logger isntance"""

    _instance: Optional['Logger'] = None

    def __new__(cls) -> 'Logger':
        """Override the __new__ method to ensure only one instance of the Logger class"""
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.setup_logger()
        return cls._instance

    def setup_logger(self) -> None:
        """Configure the logger with a default logging and adds a console logger"""
        # TODO: Custom logger for requests
        # Adjust for custom report
        # self.logger = logging.getLogger("requests")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.add_console_handler()

    def add_console_handler(self) -> None:
        """Adds a console handler to the logger with a debug log level and a custom formatter."""
        console_handler = logging.StreamHandler()
        # TODO: Adjust for custom report
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%d/%m%Y %I:%M:%S%p',
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self) -> logging.Logger:
        return self.logger


logger = Logger().get_logger()
