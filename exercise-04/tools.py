from __future__ import annotations

import ast
import operator
from datetime import datetime
from pathlib import Path


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

NOTES_FILE = DATA_DIR / "notes.txt"

MAX_NOTE_LENGTH = 500


_ALLOWED_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _evaluate_expression_node(node: ast.AST) -> float | int:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numbers are allowed.")

    if isinstance(node, ast.BinOp):
        operator_type = type(node.op)
        if operator_type not in _ALLOWED_BINARY_OPERATORS:
            raise ValueError(f"Operator {operator_type.__name__} is not allowed.")

        left = _evaluate_expression_node(node.left)
        right = _evaluate_expression_node(node.right)

        if operator_type is ast.Pow:
            if abs(right) > 10:
                raise ValueError("Exponent is too large.")

        return _ALLOWED_BINARY_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operator_type = type(node.op)
        if operator_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unary operator {operator_type.__name__} is not allowed.")

        operand = _evaluate_expression_node(node.operand)
        return _ALLOWED_UNARY_OPERATORS[operator_type](operand)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")


def calculate(expression: str) -> str:
    if not expression or not expression.strip():
        raise ValueError("Expression cannot be empty.")

    if len(expression) > 100:
        raise ValueError("Expression is too long.")

    try:
        parsed = ast.parse(expression, mode="eval")
        result = _evaluate_expression_node(parsed.body)
    except ZeroDivisionError:
        raise ValueError("Division by zero is not allowed.")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc.msg}") from exc
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"Could not evaluate expression: {exc}") from exc

    return str(result)


def save_note(text: str) -> str:
    if text is None:
        raise ValueError("Note text is required.")

    cleaned_text = text.strip()

    if not cleaned_text:
        raise ValueError("Note cannot be empty.")

    if len(cleaned_text) > MAX_NOTE_LENGTH:
        raise ValueError(f"Note is too long. Maximum length is {MAX_NOTE_LENGTH} characters.")

    if "\x00" in cleaned_text:
        raise ValueError("Note contains invalid characters.")

    with NOTES_FILE.open("a", encoding="utf-8") as file:
        file.write(cleaned_text + "\n")

    return f"Saved note to {NOTES_FILE}"


def read_notes() -> str:
    if not NOTES_FILE.exists():
        return "No notes found."

    content = NOTES_FILE.read_text(encoding="utf-8").strip()

    if not content:
        return "No notes found."

    return content