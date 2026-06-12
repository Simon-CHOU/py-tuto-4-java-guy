"""Module 01: Basics and Types — Reference Implementation."""

import re
import string


def classify_number(n):
    """Return a string describing whether n is positive/negative/zero and even/odd."""
    if not isinstance(n, int):
        raise TypeError(f"Expected int, got {type(n).__name__}")
    sign = "positive" if n > 0 else ("negative" if n < 0 else "zero")
    parity = "even" if n % 2 == 0 else "odd"
    return f"{sign} {parity}"


def safe_divide(a, b):
    """Return (quotient, remainder) for a // b. Raise ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return (a // b, a % b)


def format_table(rows):
    """Given a list of dicts with the same keys, return a formatted ASCII table string."""
    if not rows:
        return ""
    keys = list(rows[0].keys())
    col_widths = {
        key: max(len(str(key)), max(len(str(row.get(key, ""))) for row in rows)) for key in keys
    }
    header = " | ".join(str(key).ljust(col_widths[key]) for key in keys)
    separator = "-+-".join("-" * col_widths[key] for key in keys)
    body = "\n".join(
        " | ".join(str(row.get(key, "")).ljust(col_widths[key]) for key in keys) for row in rows
    )
    return f"{header}\n{separator}\n{body}"


def is_palindrome(s):
    """Return True if s is a palindrome, ignoring case, whitespace, and punctuation."""
    cleaned = re.sub(rf"[{re.escape(string.punctuation)}\s]", "", s).lower()
    return cleaned == cleaned[::-1]


def flatten_nested(nested):
    """Recursively flatten an arbitrarily nested list. Return a new flat list."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten_nested(item))
        else:
            result.append(item)
    return result


def merge_defaults(defaults, overrides):
    """Return a new dict merging defaults with overrides, without mutating inputs."""
    return {**defaults, **overrides}


def parse_command(cmd_str: str) -> str:
    """Parse a command string using structural pattern matching (match/case).

    Python 3.10+ match/case is more powerful than Java's switch — it destructures
    sequences, mappings, and class instances.
    """
    match cmd_str.split():
        case ["add", x, y]:
            return f"{x} + {y} = {int(x) + int(y)}"
        case ["quit"]:
            return "Goodbye!"
        case ["help"]:
            return "Available: add <x> <y>, quit, help"
        case _:
            return f"Unknown command: {cmd_str}"


def describe_shape(shape: dict) -> str:
    """Describe a geometric shape using dict pattern matching."""
    match shape:
        case {"type": "circle", "radius": r}:
            return f"A circle with radius {r}"
        case {"type": "rect", "w": w, "h": h}:
            return f"A {w}x{h} rectangle"
        case {"type": "point"}:
            return "A point"
        case _:
            return f"Unknown shape: {shape}"
