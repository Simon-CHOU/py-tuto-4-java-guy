"""Module 01: Basics and Types — Your Implementation."""


def classify_number(n):
    """Return a string describing whether n is positive/negative/zero and even/odd.

    Examples:
        classify_number(4)  -> "positive even"
        classify_number(-3) -> "negative odd"
        classify_number(0)  -> "zero even"
    Raises TypeError for non-int input.
    """
    raise NotImplementedError("TODO: implement classify_number")


def safe_divide(a, b):
    """Return (quotient, remainder) for a // b. Raise ValueError if b is zero.

    Python uses // for floor division and % for modulo. Together they satisfy:
        a = b * (a // b) + (a % b)

    The remainder always has the same sign as the divisor.
    """
    raise NotImplementedError("TODO: implement safe_divide")


def format_table(rows):
    """Given a list of dicts with the same keys, return a formatted ASCII table string.

    Example:
        format_table([{"name": "Alice", "score": 95}]) ->
        "name  | score\n------+------\nAlice | 95"

    Python's f-strings and str.ljust()/rjust()/center() are your friends here.
    """
    raise NotImplementedError("TODO: implement format_table")


def is_palindrome(s):
    """Return True if s is a palindrome, ignoring case, whitespace, and punctuation.

    Python strings support slicing with step: s[::-1] returns the reversed string.
    Use str.lower(), str.isalnum(), or re.sub() from the re module.
    """
    raise NotImplementedError("TODO: implement is_palindrome")


def flatten_nested(nested):
    """Recursively flatten an arbitrarily nested list. Return a new flat list.

    Example:
        flatten_nested([1, [2, [3, [4]]]]) -> [1, 2, 3, 4]

    isinstance(item, list) is the Python way to check if something is a list.
    """
    raise NotImplementedError("TODO: implement flatten_nested")


def merge_defaults(defaults, overrides):
    """Return a new dict merging defaults with overrides, without mutating inputs.

    Example:
        merge_defaults({"a": 1, "b": 2}, {"b": 3, "c": 4}) -> {"a": 1, "b": 3, "c": 4}

    Python's {**d1, **d2} syntax merges two dicts into a new one. Keys in d2 override d1.
    This is the Python idiom for "copy with updates" — no need for a builder pattern.
    """
    raise NotImplementedError("TODO: implement merge_defaults")
