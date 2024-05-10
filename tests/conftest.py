import pytest


@pytest.fixture(scope='module')
def base_url():
    return 'https://jsonplaceholder.typicode.com'
