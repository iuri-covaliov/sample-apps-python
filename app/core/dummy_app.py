from app.core.appcontext import AppContext
from app.services.calculator import Calculator


_GREATING_TEMPLATE = """
=======================================================
-------------------------------------------------------
=======================================================

Welcome to {} v{}!
I am your dummy application.
Description: {}

I will not listen to any pert.
I will do absolutely nothing until you shut me down.
Use ctrl+c to exit.

=======================================================
-------------------------------------------------------
=======================================================
"""


class DummyApp:
    """A dummey application to simulate a real app behavior."""

    def __init__(self, context: AppContext) -> None:
        self.context = context

    def print_greating(self) -> None:
        app_name = self.context.settings.APP.NAME
        app_version = self.context.settings.APP.VERSION
        app_description = self.context.settings.APP.DESCRIPTION

        print(_GREATING_TEMPLATE.format(app_name, app_version, app_description))

    def do_math(self, calc: Calculator = Calculator()) -> None:
        logger = self.context.logger

        logger.info("Addition: %s", calc.add(10, 5))
        logger.info("Subtraction: %s", calc.subtract(10, 5))
        logger.info("Multiplication: %s", calc.multiply(10, 5))
        logger.info("Division: %s", calc.divide(10, 5))

    def run(self) -> None:
        self.print_greating()
        while True:
            pass  # Keep the app running
