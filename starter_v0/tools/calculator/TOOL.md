---
name: calculator
track: bonus
kind: local_formatter
provider: Python AST
requires_env: []
inputs: [expression]
outputs: [tool, expression, result, error, message]
side_effect: false
---

# Calculator

Safely evaluates bounded numeric arithmetic locally. Supported operators are
`+`, `-`, `*`, `/`, `//`, `%`, `**`, parentheses, and unary signs.

The implementation uses a strict AST allowlist instead of Python `eval()`.
It rejects names, calls, attributes, containers, strings, booleans, oversized
expressions, very large values, and unsafe exponents. It does not perform
symbolic algebra, calculus, proofs, unit conversion, or currency conversion.
