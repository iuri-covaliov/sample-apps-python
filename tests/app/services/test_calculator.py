from contextlib import nullcontext as does_not_raise

from app.services.calculator import Calculator, check_numbers
import pytest
from typing import Any, Union


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
        check_numbers(a, b)

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
            check_numbers(a, b)


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
            pytest.param(1, 2, 0.5, does_not_raise(), id="1, 2, 0.5, No Exception"),
            pytest.param(4, -2, -2, does_not_raise(), id="4, -2, -2, No Exception"),
            pytest.param(
                2.5, 2, 1.25, does_not_raise(), id="2.5, 2, 1.25, No Exception"
            ),
            pytest.param(2, 0, 0, pytest.raises(ValueError), id="2, 0, 0, ValueError"),
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
