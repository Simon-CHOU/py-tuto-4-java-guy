"""Tests for Module 01: Basics and Types."""

import pytest
from practice import (
    classify_number,
    describe_shape,
    flatten_nested,
    format_table,
    is_palindrome,
    merge_defaults,
    parse_command,
    safe_divide,
)


class TestClassifyNumber:
    def test_positive_even(self):
        assert classify_number(4) == "positive even"

    def test_positive_odd(self):
        assert classify_number(7) == "positive odd"

    def test_negative_even(self):
        assert classify_number(-6) == "negative even"

    def test_negative_odd(self):
        assert classify_number(-3) == "negative odd"

    def test_zero(self):
        assert classify_number(0) == "zero even"

    def test_type_error_on_float(self):
        with pytest.raises(TypeError):
            classify_number(3.14)

    def test_type_error_on_str(self):
        with pytest.raises(TypeError):
            classify_number("42")


class TestSafeDivide:
    def test_normal_division(self):
        assert safe_divide(10, 3) == (3, 1)

    def test_exact_division(self):
        assert safe_divide(10, 2) == (5, 0)

    def test_division_by_zero(self):
        with pytest.raises(ValueError, match="zero"):
            safe_divide(5, 0)

    def test_negative_dividend(self):
        assert safe_divide(-10, 3) == (-4, 2)

    def test_both_negative(self):
        assert safe_divide(-10, -3) == (3, -1)


class TestFormatTable:
    def test_basic_table(self):
        data = [
            {"name": "Alice", "score": 95},
            {"name": "Bob", "score": 87},
        ]
        result = format_table(data)
        assert "Alice" in result
        assert "95" in result
        assert "Bob" in result
        assert "87" in result

    def test_empty_list(self):
        assert format_table([]) == ""

    def test_single_row(self):
        data = [{"name": "Alice", "score": 95}]
        result = format_table(data)
        assert "Alice" in result
        assert "95" in result


class TestIsPalindrome:
    def test_simple_palindrome(self):
        assert is_palindrome("racecar") is True

    def test_not_palindrome(self):
        assert is_palindrome("hello") is False

    def test_ignore_case_and_spaces(self):
        assert is_palindrome("A man a plan a canal Panama") is True

    def test_ignore_punctuation(self):
        assert is_palindrome("Was it a car or a cat I saw?") is True

    def test_empty_string(self):
        assert is_palindrome("") is True

    def test_single_char(self):
        assert is_palindrome("a") is True


class TestFlattenNested:
    def test_already_flat(self):
        assert flatten_nested([1, 2, 3]) == [1, 2, 3]

    def test_one_level(self):
        assert flatten_nested([1, [2, 3], 4]) == [1, 2, 3, 4]

    def test_deeply_nested(self):
        assert flatten_nested([1, [2, [3, [4]]]]) == [1, 2, 3, 4]

    def test_empty_list(self):
        assert flatten_nested([]) == []

    def test_mixed_empty_sublists(self):
        assert flatten_nested([1, [], [2, []]]) == [1, 2]


class TestMergeDefaults:
    def test_merge_overrides(self):
        defaults = {"a": 1, "b": 2}
        overrides = {"b": 3, "c": 4}
        result = merge_defaults(defaults, overrides)
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_defaults_not_mutated(self):
        defaults = {"a": 1}
        overrides = {"a": 2, "b": 3}
        merge_defaults(defaults, overrides)
        assert defaults == {"a": 1}

    def test_no_overrides(self):
        defaults = {"a": 1, "b": 2}
        result = merge_defaults(defaults, {})
        assert result == {"a": 1, "b": 2}
        assert result is not defaults  # new dict, not same reference


class TestParseCommand:
    def test_add(self):
        assert parse_command("add 3 4") == "3 + 4 = 7"

    def test_add_negative(self):
        assert parse_command("add -1 5") == "-1 + 5 = 4"

    def test_quit(self):
        assert parse_command("quit") == "Goodbye!"

    def test_help(self):
        result = parse_command("help")
        assert "add" in result
        assert "quit" in result
        assert "help" in result

    def test_unknown(self):
        result = parse_command("fly to moon")
        assert "Unknown command" in result


class TestDescribeShape:
    def test_circle(self):
        assert describe_shape({"type": "circle", "radius": 5}) == "A circle with radius 5"

    def test_rectangle(self):
        result = describe_shape({"type": "rect", "w": 10, "h": 20})
        assert result == "A 10x20 rectangle"

    def test_point(self):
        assert describe_shape({"type": "point"}) == "A point"

    def test_unknown_shape(self):
        result = describe_shape({"type": "blob"})
        assert "Unknown shape" in result
