from logging import Logger

from app.core.config import Settings


class AppContext:
    def __init__(self, settings: Settings, logger: Logger) -> None:
        self.settings = settings
        self.logger = logger
