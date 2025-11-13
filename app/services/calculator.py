from typing import Union


def check_numbers(a: Union[int, float], b: Union[int, float]) -> None:
    """Check if the values are numbers (int or float)."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be int or float.")


class Calculator:
    """Simple calculator class to perform basic arithmetic operations."""

    @staticmethod
    def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Return the sum of two numbers."""
        check_numbers(a, b)
        return a + b

    @staticmethod
    def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Return the difference of two numbers."""
        check_numbers(a, b)
        return a - b

    @staticmethod
    def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Return the product of two numbers."""
        check_numbers(a, b)
        return a * b

    @staticmethod
    def divide(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Return the quotient of two numbers. Raises ValueError on division by zero."""
        check_numbers(a, b)
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b
