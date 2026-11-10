"""Offline tests for the TV3 calculator tool."""
from __future__ import annotations

import pytest

from tools import TOOL_FUNCTIONS


calculator = TOOL_FUNCTIONS["calculator"]


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("125 + 75 - 20", 180),
        ("120 / 6 * 3", 60),
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("-2.5 * 4", -10.0),
        ("1200 * 15 / 100", 180),
        ("2 ** 10", 1024),
        ("17 // 5", 3),
        ("17 % 5", 2),
    ],
)
def test_calculator_evaluates_supported_arithmetic(expression: str, expected: int | float) -> None:
    assert calculator(expression) == {
        "tool": "calculator",
        "expression": expression,
        "result": expected,
    }


@pytest.mark.parametrize("expression", ["", "   ", "2 + * 3", "10 / 0", "10 // 0", "10 % 0"])
def test_calculator_returns_error_dict_for_bad_arithmetic(expression: str) -> None:
    result = calculator(expression)
    assert result["tool"] == "calculator"
    assert "error" in result
    assert "message" in result


@pytest.mark.parametrize("expression", [None, 123, ["1", "+", "2"]])
def test_calculator_rejects_non_string_input(expression: object) -> None:
    result = calculator(expression)  # type: ignore[arg-type]
    assert result["error"] == "TypeError"


@pytest.mark.parametrize(
    "expression",
    [
        "__import__('os').system('dir')",
        "x + 1",
        "(1).__class__",
        "[1, 2, 3]",
        "{'value': 1}",
        "'abc' * 10",
        "True + 1",
    ],
)
def test_calculator_rejects_unsafe_or_non_numeric_expression(expression: str) -> None:
    result = calculator(expression)
    assert result["error"] == "ValueError"


def test_calculator_rejects_oversized_expression() -> None:
    result = calculator("1" * 201)
    assert result["error"] == "ValueError"


def test_calculator_rejects_unsafe_exponent_and_large_result() -> None:
    assert calculator("2 ** 101")["error"] == "ValueError"
    assert calculator("10 ** 100")["error"] == "ValueError"
    assert calculator("100 ** 100")["error"] == "ValueError"
