"""Module 03: OOP — Reference Implementation."""

import math


class Vector2D:
    """Immutable 2D vector with dunder methods."""

    __slots__ = ("_x", "_y")

    def __init__(self, x, y):
        object.__setattr__(self, "_x", x)
        object.__setattr__(self, "_y", y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x - other.x, self.y - other.y)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __hash__(self):
        return hash((self.x, self.y))

    def __setattr__(self, name, value):
        raise AttributeError("Vector2D is immutable")


class BetterDict(dict):
    """A dict subclass that allows attribute-style access."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'BetterDict' has no key '{name}'") from None

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'BetterDict' has no key '{name}'") from None


class Temperature:
    """Temperature with property-based celsius/fahrenheit conversion."""

    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5 / 9


class ImmutableConfig:
    """A configuration object that freezes after __init__."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    def __setattr__(self, name, value):
        raise AttributeError(f"Cannot modify attribute '{name}' — object is immutable")

    def __repr__(self):
        items = dict(self.__dict__.items())
        return f"ImmutableConfig({items})"


from dataclasses import dataclass  # noqa: E402


@dataclass(frozen=True)
class ConfigRecord:
    """Immutable configuration using @dataclass(frozen=True).

    Python dataclasses are the closest equivalent to Java records.
    @dataclass auto-generates __init__, __repr__, __eq__, and __hash__.
    frozen=True makes instances immutable.
    """

    host: str = "localhost"
    port: int = 8080
    debug: bool = False
