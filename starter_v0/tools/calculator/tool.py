"""Safe local arithmetic calculator for numeric research calculations."""
from __future__ import annotations

import ast
import math
import operator
from typing import Any, Callable

from tools._shared import err


MAX_EXPRESSION_LENGTH = 200
MAX_AST_NODES = 64
MAX_ABS_VALUE = 1e100
MAX_ABS_EXPONENT = 100

_BINARY_OPERATORS: dict[type[ast.operator], Callable[[int | float, int | float], int | float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[int | float], int | float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _checked_number(value: Any) -> int | float:
    """Allow only bounded finite real numbers, never bool/complex/string values."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Only real numeric literals are allowed")
    if isinstance(value, int) and len(str(abs(value))) > 100:
        raise ValueError("Integer value is too large")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Non-finite numbers are not allowed")
    if abs(value) > MAX_ABS_VALUE:
        raise ValueError("Numeric value is too large")
    return value


def _evaluate(node: ast.AST) -> int | float:
    if isinstance(node, ast.Constant):
        return _checked_number(node.value)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        value = _evaluate(node.operand)
        return _checked_number(_UNARY_OPERATORS[type(node.op)](value))

    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > MAX_ABS_EXPONENT:
            raise ValueError(f"Exponent must be between -{MAX_ABS_EXPONENT} and {MAX_ABS_EXPONENT}")
        result = _BINARY_OPERATORS[type(node.op)](left, right)
        return _checked_number(result)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")


def calculate(expression: str = "") -> dict[str, Any]:
    """Evaluate a bounded arithmetic expression without Python ``eval``."""
    try:
        if not isinstance(expression, str):
            raise TypeError("expression must be a string")
        expression = expression.strip()
        if not expression:
            raise ValueError("expression must not be empty")
        if len(expression) > MAX_EXPRESSION_LENGTH:
            raise ValueError(f"expression must be at most {MAX_EXPRESSION_LENGTH} characters")

        tree = ast.parse(expression, mode="eval")
        if sum(1 for _ in ast.walk(tree)) > MAX_AST_NODES:
            raise ValueError(f"expression is too complex (maximum {MAX_AST_NODES} syntax nodes)")

        result = _evaluate(tree.body)
        return {"tool": "calculator", "expression": expression, "result": result}
    except Exception as exc:
        return err("calculator", exc)
