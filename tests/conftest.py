import os

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("API_BASE_URL")


def pytest_html_report_title(report):
    report.title = f"{os.getenv('PROJECT_NAME')} - Test Report"
