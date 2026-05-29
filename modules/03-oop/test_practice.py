"""Tests for Module 03: Object-Oriented Programming."""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

import math
import pytest
from practice import Vector2D, BetterDict, Temperature, ImmutableConfig


class TestVector2D:
    def test_init_and_repr(self):
        v = Vector2D(3, 4)
        assert repr(v) == "Vector2D(3, 4)"

    def test_equality(self):
        assert Vector2D(1, 2) == Vector2D(1, 2)
        assert Vector2D(1, 2) != Vector2D(3, 4)
        assert Vector2D(1, 2) != "not a vector"

    def test_add(self):
        v1 = Vector2D(1, 2)
        v2 = Vector2D(3, 4)
        assert v1 + v2 == Vector2D(4, 6)

    def test_sub(self):
        v1 = Vector2D(5, 7)
        v2 = Vector2D(2, 3)
        assert v1 - v2 == Vector2D(3, 4)

    def test_abs(self):
        v = Vector2D(3, 4)
        assert abs(v) == 5.0

    def test_bool(self):
        assert bool(Vector2D(1, 0)) is True
        assert bool(Vector2D(0, 0)) is False

    def test_immutable(self):
        v = Vector2D(1, 2)
        with pytest.raises(AttributeError):
            v.x = 5


class TestBetterDict:
    def test_dot_access(self):
        d = BetterDict({"name": "Alice", "age": 30})
        assert d.name == "Alice"
        assert d.age == 30

    def test_key_fallback(self):
        d = BetterDict({"name": "Alice"})
        assert d["name"] == "Alice"

    def test_missing_attribute(self):
        d = BetterDict({"name": "Alice"})
        with pytest.raises(AttributeError):
            _ = d.nonexistent


class TestTemperature:
    def test_celsius_getter(self):
        t = Temperature(celsius=0)
        assert t.celsius == 0

    def test_fahrenheit_getter(self):
        t = Temperature(celsius=0)
        assert t.fahrenheit == 32.0

    def test_fahrenheit_setter(self):
        t = Temperature(celsius=0)
        t.fahrenheit = 212
        assert t.celsius == 100.0

    def test_celsius_setter(self):
        t = Temperature(celsius=0)
        t.celsius = 100
        assert t.fahrenheit == 212.0


class TestImmutableConfig:
    def test_init_with_kwargs(self):
        c = ImmutableConfig(host="localhost", port=8080)
        assert c.host == "localhost"
        assert c.port == 8080

    def test_prevent_mutation(self):
        c = ImmutableConfig(host="localhost")
        with pytest.raises(AttributeError):
            c.host = "other"

    def test_prevent_new_attr(self):
        c = ImmutableConfig(host="localhost")
        with pytest.raises(AttributeError):
            c.new_attr = 42
