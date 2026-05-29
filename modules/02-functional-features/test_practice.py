"""Tests for Module 02: Functional Features."""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

import pytest
from practice import (
    select_and_transform,
    word_frequencies,
    fibonacci,
    group_by,
    running_average,
    interleave,
)


class TestSelectAndTransform:
    def test_filter_and_square(self):
        result = select_and_transform(
            [1, 2, 3, 4, 5, 6],
            predicate=lambda x: x > 3,
            transform=lambda x: x ** 2,
        )
        assert result == [16, 25, 36]

    def test_all_pass(self):
        assert select_and_transform([1, 2, 3], lambda x: True, lambda x: x * 2) == [2, 4, 6]

    def test_none_pass(self):
        assert select_and_transform([1, 2, 3], lambda x: x > 10, lambda x: x * 2) == []

    def test_returns_list_not_generator(self):
        result = select_and_transform([1, 2], lambda x: True, lambda x: x)
        assert isinstance(result, list)


class TestWordFrequencies:
    def test_simple(self):
        result = word_frequencies("hello world hello")
        assert result == {"hello": 2, "world": 1}

    def test_case_insensitive(self):
        result = word_frequencies("Hello hello HELLO")
        assert result == {"hello": 3}

    def test_ignores_punctuation(self):
        result = word_frequencies("hello! world? hello.")
        assert result == {"hello": 2, "world": 1}

    def test_empty_string(self):
        assert word_frequencies("") == {}


class TestFibonacci:
    def test_first_ten(self):
        gen = fibonacci()
        first_ten = [next(gen) for _ in range(10)]
        assert first_ten == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_is_generator(self):
        import types
        assert isinstance(fibonacci(), types.GeneratorType)


class TestGroupBy:
    def test_by_length(self):
        words = ["cat", "dog", "bird", "fish", "elephant"]
        result = group_by(words, len)
        assert result == {3: ["cat", "dog"], 4: ["bird", "fish"], 8: ["elephant"]}

    def test_by_first_letter(self):
        words = ["apple", "ant", "banana", "bat"]
        result = group_by(words, lambda w: w[0])
        assert result == {"a": ["apple", "ant"], "b": ["banana", "bat"]}

    def test_empty_list(self):
        assert group_by([], len) == {}


class TestRunningAverage:
    def test_sequence(self):
        result = list(running_average([2, 4, 6, 8]))
        assert result == [2.0, 3.0, 4.0, 5.0]

    def test_single_element(self):
        assert list(running_average([42])) == [42.0]

    def test_empty(self):
        assert list(running_average([])) == []

    def test_is_generator(self):
        import types
        assert isinstance(running_average([1]), types.GeneratorType)


class TestInterleave:
    def test_two_lists(self):
        result = list(interleave([1, 2, 3], ["a", "b", "c"]))
        assert result == [1, "a", 2, "b", 3, "c"]

    def test_unequal_lengths(self):
        result = list(interleave([1, 2, 3, 4], ["a"]))
        assert result == [1, "a", 2, 3, 4]

    def test_empty_iterable(self):
        result = list(interleave([], [1, 2, 3]))
        assert result == [1, 2, 3]

    def test_is_generator(self):
        import types
        assert isinstance(interleave([1], [2]), types.GeneratorType)
