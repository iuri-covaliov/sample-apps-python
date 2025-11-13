from contextlib import nullcontext as does_not_raise
from typing import Any, Union
from unittest.mock import MagicMock, patch

import pytest

from app.services.calculator import Calculator, main
from tests.conftest import AppContext


class TestCheckNumbers:
    @pytest.mark.parametrize(
        "a, b",
        [
            (1, 2),
            (1.5, 2.5),
            (-1, -2),
            (0, 0),
        ],
    )
    def test_valid_numbers(self, a: Union[int, float], b: Union[int, float]) -> None:
        # Should not raise any exception
        Calculator.add(a, b)

    @pytest.mark.parametrize(
        "a, b",
        [
            ("1", 2),
            (1, "2"),
            (None, 2),
            (1, []),
        ],
    )
    def test_invalid_numbers(self, a: Any, b: Any) -> None:
        with pytest.raises(TypeError):
            Calculator.add(a, b)


class TestCalculator:
    @pytest.mark.parametrize(
        "a, b, expected_result",
        [
            (1, 2, 3),
            (1, -2, -1),
            (2.5, 2.5, 5.0),
        ],
    )
    def test_add(
        self,
        a: Union[int, float],
        b: Union[int, float],
        expected_result: Union[int, float],
    ) -> None:
        assert Calculator.add(a, b) == expected_result

    @pytest.mark.parametrize(
        "a, b, expected_result",
        [
            (1, 2, -1),
            (1, -2, 3),
            (2.5, 2.5, 0.0),
        ],
    )
    def test_subtract(
        self,
        a: Union[int, float],
        b: Union[int, float],
        expected_result: Union[int, float],
    ) -> None:
        assert Calculator.subtract(a, b) == expected_result

    @pytest.mark.parametrize(
        "a, b, expected_result",
        [
            (1, 2, 2),
            (1, -2, -2),
            (2.5, 2.5, 6.25),
        ],
    )
    def test_multiply(
        self,
        a: Union[int, float],
        b: Union[int, float],
        expected_result: Union[int, float],
    ) -> None:
        assert Calculator.multiply(a, b) == expected_result

    @pytest.mark.parametrize(
        "a, b, expected_result, expectation",
        [
            (1, 2, 0.5, does_not_raise()),
            (4, -2, -2, does_not_raise()),
            (2.5, 2, 1.25, does_not_raise()),
            (2, 0, 0, pytest.raises(ValueError)),
        ],
    )
    def test_divide(
        self,
        a: Union[int, float],
        b: Union[int, float],
        expected_result: Union[int, float],
        expectation: Any,
    ) -> None:
        with expectation:
            assert Calculator.divide(a, b) == expected_result


class TestMain:
    """Test the main function behavior."""

    @patch("app.services.calculator.setup_logging")
    @patch("app.services.calculator.get_logger")
    @patch("builtins.print")
    def test_main_function_calls_and_logging(
        self,
        mock_print: Any,
        mock_get_logger: Any,
        mock_setup_logging: Any,
        app_context: AppContext,
    ) -> None:
        """Test that main function initializes settings, logging, etc."""
        # Mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Call main function
        main()

        # Verify print was called with log level (defaults from Settings)
        mock_print.assert_called_once_with("App Settings. Log level: ", "DEBUG")

        # Verify setup_logging was called with correct parameters (defaults)
        mock_setup_logging.assert_called_once_with(
            level="DEBUG",
            fmt="[%(levelname)s|%(module)s|line:%(lineno)d] %(asctime)s: %(message)s",
            date_fmt="%Y-%m-%d %H:%M:%S",
        )

        # Verify get_logger was called
        mock_get_logger.assert_called_once_with("app.services.calculator")

        # Check logger calls
        assert mock_logger.info.call_count == 6
        assert mock_logger.warning.call_count == 1
        assert mock_logger.error.call_count == 1
        assert mock_logger.debug.call_count == 1

        # Check specific logger calls
        mock_logger.warning.assert_called_with("This is a warning message.")
        mock_logger.error.assert_called_with("This is an error message.")
        mock_logger.debug.assert_called_with("Logging correctly set to DEBUG level.")
