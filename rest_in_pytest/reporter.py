from __future__ import annotations

import os

from jinja2 import Environment, FileSystemLoader
from pytest_html import HTMLReporter


class Reporter(HTMLReporter):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.template_env = Environment(
            loader=FileSystemLoader(
                os.path.join(os.path.dirname(__file__), 'templates')
            )
        )
        self.template = self.env.get_template('report.html')

    # TODO Generate report with custom styling
