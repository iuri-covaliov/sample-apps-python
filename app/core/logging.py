import logging


def setup_logging(level: str, fmt: str, date_fmt: str) -> None:
    """Set up logging configuration."""
    # Force configuration even if logging was already initialized
    root_logger = logging.getLogger()

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Set up new configuration
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=fmt,
        datefmt=date_fmt,
        force=True,  # Force reconfiguration
    )

    # Explicitly set root logger level to ensure it takes effect
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
