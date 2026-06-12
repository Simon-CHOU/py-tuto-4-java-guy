"""Tests for Module 07: Type Hints."""

import pytest
from practice import Stack, first, typed_deserialize


class TestStack:
    def test_push_pop_int(self):
        s = Stack[int]()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        assert s.pop() == 1

    def test_push_pop_str(self):
        s = Stack[str]()
        s.push("a")
        s.push("b")
        assert s.pop() == "b"

    def test_empty_raises(self):
        s = Stack[int]()
        with pytest.raises(IndexError, match="empty"):
            s.pop()

    def test_len(self):
        s = Stack[int]()
        s.push(1)
        s.push(2)
        assert len(s) == 2

    def test_bool(self):
        s = Stack[int]()
        assert bool(s) is False
        s.push(1)
        assert bool(s) is True


class TestFirst:
    def test_non_empty_list(self):
        result = first([1, 2, 3])
        assert result == 1

    def test_empty_returns_none(self):
        assert first([]) is None

    def test_strings(self):
        assert first(["hello", "world"]) == "hello"


class TestTypedDeserialize:
    def test_basic_dict(self):
        data = {"name": "Alice", "age": 30}
        result = typed_deserialize(data, dict)
        assert result["name"] == "Alice"
        assert result["age"] == 30

    def test_int_coercion(self):
        result = typed_deserialize(42, str)
        assert result == "42"

    def test_list_element_coercion(self):
        result = typed_deserialize(["1", "2", "3"], list[int])
        assert result == [1, 2, 3]
