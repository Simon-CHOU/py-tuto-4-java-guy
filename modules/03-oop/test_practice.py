"""Tests for Module 03: Object-Oriented Programming."""

import pytest
from practice import BetterDict, ConfigRecord, ImmutableConfig, Temperature, Vector2D


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

    def test_hashable(self):
        v1 = Vector2D(1, 2)
        v2 = Vector2D(1, 2)
        v3 = Vector2D(3, 4)
        s = {v1, v2, v3}
        assert len(s) == 2  # v1 and v2 are equal, so one hash collision

    def test_dict_key(self):
        v = Vector2D(0, 0)
        d = {v: "origin"}
        assert d[Vector2D(0, 0)] == "origin"


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


class TestConfigRecord:
    def test_init_defaults(self):
        c = ConfigRecord()
        assert c.host == "localhost"
        assert c.port == 8080
        assert c.debug is False

    def test_init_custom(self):
        c = ConfigRecord(host="example.com", port=443, debug=True)
        assert c.host == "example.com"
        assert c.port == 443
        assert c.debug is True

    def test_immutable(self):
        c = ConfigRecord()
        with pytest.raises(AttributeError):
            c.host = "other"

    def test_equality(self):
        c1 = ConfigRecord(host="a", port=1)
        c2 = ConfigRecord(host="a", port=1)
        assert c1 == c2
        assert c1 != ConfigRecord(host="b", port=1)

    def test_hashable(self):
        c = ConfigRecord()
        s = {c}
        assert c in s

    def test_repr(self):
        c = ConfigRecord(host="x", port=1, debug=False)
        r = repr(c)
        assert "x" in r
        assert "1" in r
