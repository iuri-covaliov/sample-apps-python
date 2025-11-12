from typing import Iterator
from unittest.mock import patch

import pytest

MOCK_ENV_VARS = {
    "APP_NAME": "Test Python App",
    "APP_VERSION": "0.0.1-test",
}


@pytest.fixture(scope="module")
def test_env() -> Iterator[None]:
    """Fixture to set up test environment variables."""  # noqa: E501
    with patch.dict("os.environ", MOCK_ENV_VARS):
        yield
