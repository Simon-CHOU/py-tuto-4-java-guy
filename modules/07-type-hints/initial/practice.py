"""Module 07: Type Hints — Your Implementation."""


# TODO: import Generic, TypeVar, Sequence, get_origin, get_args from typing

T = TypeVar("T")


class Stack(Generic[T]):
    """A generic stack.

    Stack[int] creates a stack of integers, Stack[str] for strings.
    The [T] syntax uses TypeVar — think of it as Java's <T> in generics.

    Java analogy: public class Stack<T> { private List<T> items; ... }
    """
    raise NotImplementedError("TODO: implement Stack")


def first(items: Sequence[T]) -> T | None:
    """Return the first element of a sequence, or None if empty.

    Sequence is a read-only protocol — list, tuple, str, bytes, range all satisfy it.
    T | None is Python 3.10+ syntax for Optional[T] (Java's @Nullable).
    """
    raise NotImplementedError("TODO: implement first")


def typed_deserialize(data, target_type):
    """Coerce data to the target type.

    Use get_origin() and get_args() from the typing module to inspect
    generic types at runtime.

    Example:
        typed_deserialize(["1", "2"], list[int]) -> [1, 2]
        typed_deserialize(42, str) -> "42"
    """
    raise NotImplementedError("TODO: implement typed_deserialize")
