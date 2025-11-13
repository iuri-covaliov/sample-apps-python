from http.server import HTTPServer
import logging
from typing import Any

from app.core.api import API
from app.core.config import Settings
from app.core.logging import get_logger, setup_logging


def create_app(settings: Settings, logger: logging.Logger) -> API:
    """Create and configure the API application."""

    logger.info(f"Initializing {settings.APP.NAME} version {settings.APP.VERSION}")
    api = API()

    @api.get("/")
    def get_index(args: Any) -> dict[str, Any]:
        return {
            "name": settings.APP.NAME,
            "description": settings.APP.DESCRIPTION,
            "actions": ["health"],
            "version": settings.APP.VERSION,
        }

    @api.get("/health")
    def get_health(args: Any) -> dict[str, Any]:
        return {"status": "healthy"}

    logger.info("API application created successfully.")

    return api


def create_server(settings: Settings, logger: logging.Logger) -> HTTPServer:
    api = create_app(settings, logger)
    PORT = settings.APP.PORT

    logger.info(f"Starting httpd server on 0.0.0.0:{PORT}")
    httpd = HTTPServer(("0.0.0.0", PORT), api)
    logger.info(f"httpd server started at http://0.0.0.0:{PORT}/")

    return httpd


def main() -> None:
    settings = Settings()
    print("Setting up the application...")

    setup_logging(
        level=settings.LOGGING.LEVEL,
        fmt=settings.LOGGING.FORMAT,
        date_fmt=settings.LOGGING.DATE_FORMAT,
    )

    logger = get_logger(__name__)

    httpd = create_server(settings, logger)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
