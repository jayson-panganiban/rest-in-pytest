import logging
import os
import pytest
from dotenv import load_dotenv
from pytest_metadata.plugin import metadata_key

load_dotenv()

PROJECT_NAME = f"{os.getenv('PROJECT_NAME')}"


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("API_BASE_URL")


def pytest_html_report_title(report):
    report.title = f"{PROJECT_NAME} - Test Report"


def pytest_configure(config):
    config.stash[metadata_key]["Project"] = PROJECT_NAME


@pytest.fixture(autouse=True)
def configure_logging(caplog):
    caplog.set_level(logging.INFO)
