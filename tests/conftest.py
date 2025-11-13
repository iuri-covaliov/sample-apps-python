from typing import Iterator
from unittest.mock import patch

import pytest

from app.core.appcontext import AppContext
from app.core.config import Settings
from app.core.logging import setup_logging, get_logger

MOCK_ENV_VARS = {
    "APP_NAME": "Test Python App",
    "APP_VERSION": "0.0.1-test",
}


@pytest.fixture(scope="session")
def app_context() -> Iterator[AppContext]:
    """Fixture to set up test environment variables."""  # noqa: E501
    with patch.dict("os.environ", MOCK_ENV_VARS):
        settings = Settings()
        setup_logging(
            level=settings.LOGGING.LEVEL,
            fmt=settings.LOGGING.FORMAT,
            date_fmt=settings.LOGGING.DATE_FORMAT,
        )
        logger = get_logger("tests.conftest")
        logger.info("Setting up application context for tests...")
        context = AppContext(settings=settings, logger=logger)
        yield context

        # Teardown can be handled here if necessary
