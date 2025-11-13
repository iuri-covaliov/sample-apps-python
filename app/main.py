from app.core.config import Settings
from app.core.appcontext import AppContext
from app.core.dummy_app import DummyApp as App
from app.core.logging import setup_logging, get_logger


def create_app_context() -> AppContext:
    print("Initializing application context...")
    settings = Settings()

    setup_logging(
        level=settings.LOGGING.LEVEL,
        fmt=settings.LOGGING.FORMAT,
        date_fmt=settings.LOGGING.DATE_FORMAT,
    )

    logger = get_logger(__name__)
    logger.info("Application context initialized.")

    return AppContext(settings=settings, logger=logger)


def create_app(context: AppContext | None = None) -> App:
    if context is None:
        context = create_app_context()

    logger = context.logger
    logger.info("Creating App instance...")
    app = App(context)
    logger.info("App instance created.")

    return app


def main() -> None:
    context = create_app_context()
    app = create_app(context=context)
    logger = app.context.logger

    logger.info("Performing sample calculations...")
    app.do_math()

    logger.info("Starting the application...")
    app.run()


if __name__ == "__main__":
    main()
