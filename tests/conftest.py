from logging import Logger
from typing import Iterator
from unittest.mock import patch

import pytest

from app.main import create_app
from app.core.apiTestClient import APITestClient
from app.core.config import Settings
from app.core.logging import get_logger, setup_logging

MOCK_ENV_VARS: dict[str, str] = {
    "APP_NAME": "Test Python App",
    "APP_DESCRIPTION": "A test description for the Python app.",
    "APP_VERSION": "0.0.1-test",
}


class AppContext:
    settings: Settings
    logger: Logger

    def __init__(self, settings: Settings, logger: Logger) -> None:
        self.settings = settings
        self.logger = logger


@pytest.fixture(scope="module")
def app_context() -> Iterator[AppContext]:
    """Fixture to set up test environment variables."""  # noqa: E501
    with patch.dict("os.environ", MOCK_ENV_VARS):
        settings = Settings()
        setup_logging(
            level=settings.LOGGING.LEVEL,
            fmt=settings.LOGGING.FORMAT,
            date_fmt=settings.LOGGING.DATE_FORMAT,
        )
        logger = get_logger("test_client")

        app_context = AppContext(settings, logger)

        yield app_context


@pytest.fixture
def client(app_context: AppContext) -> APITestClient:
    """Fixture to provide an APITestClient instance."""
    api = create_app(app_context.settings, app_context.logger)
    return APITestClient(api)
