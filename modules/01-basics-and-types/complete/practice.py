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
        key: max(len(str(key)), max(len(str(row.get(key, ""))) for row in rows))
        for key in keys
    }
    header = " | ".join(str(key).ljust(col_widths[key]) for key in keys)
    separator = "-+-".join("-" * col_widths[key] for key in keys)
    body = "\n".join(
        " | ".join(str(row.get(key, "")).ljust(col_widths[key]) for key in keys)
        for row in rows
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
