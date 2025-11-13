import logging

from app.core.config import Settings
from app.core.logging import get_logger, setup_logging


class TestSetupLogging:
    def test_setup_logging_from_settings(self) -> None:
        settings = Settings()
        setup_logging(
            level=settings.LOGGING.LEVEL,
            fmt=settings.LOGGING.FORMAT,
            date_fmt=settings.LOGGING.DATE_FORMAT,
        )

        logger = get_logger("test_logger")
        # Use getEffectiveLevel() instead of level to get the actual logging level
        logger_level = logging.getLevelName(logger.getEffectiveLevel())

        assert logger_level == settings.LOGGING.LEVEL.upper()
