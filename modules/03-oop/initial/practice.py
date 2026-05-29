"""Module 03: OOP — Your Implementation."""


class Vector2D:
    """Immutable 2D vector.

    Implement: __init__, __repr__, __eq__, __add__, __sub__, __abs__, __bool__
    Use __slots__ for memory efficiency.

    Java analogy: Java's record class or a final class with equals/hashCode/toString,
    but in Python you hook into the language via dunder (double-underscore) methods.
    """
    raise NotImplementedError("TODO: implement Vector2D")


class BetterDict(dict):
    """A dict subclass that allows attribute-style access (d.key in addition to d['key']).

    Java analogy: No direct equivalent, but think of it as a Map that also
    supports getX() style access — except Python makes it transparent.
    """
    raise NotImplementedError("TODO: implement BetterDict")


class Temperature:
    """Temperature with property-based celsius/fahrenheit conversion.

    Python's @property replaces Java's getter/setter pattern.
    No need for getCelsius()/setCelsius() — just direct attribute access
    that invokes your methods transparently.
    """
    raise NotImplementedError("TODO: implement Temperature")


class ImmutableConfig:
    """A configuration object that freezes after __init__.

    Override __setattr__ to prevent mutation. This is Python's way
    of creating read-only objects. Compare with Java's final fields
    or Collections.unmodifiableX()."""
    raise NotImplementedError("TODO: implement ImmutableConfig")
