from datetime import datetime


def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate(expression: str) -> str:
    allowed_chars = "0123456789+-*/(). "
    if any(char not in allowed_chars for char in expression):
        raise ValueError("Expression contains invalid characters.")

    try:
        # BEWARE: THIS CODE ALLOWS EXECUTION OF ALMOST ANY COMMAND ON YOUR
        # COMPUTER! THIS IS FOR EDUCATIONAL PURPOSES ONLY!
        result = eval(expression, {"__builtins__": {}}, {})
    except Exception as e:
        raise ValueError(f"Could not calculate expression: {e}")

    return str(result)


def save_note(text: str) -> str:
    filename = "notes.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(text.strip() + "\n")
    return f"Saved note to {filename}"