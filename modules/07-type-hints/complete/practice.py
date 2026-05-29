"""Module 07: Type Hints — Reference Implementation."""

from typing import Generic, TypeVar, Sequence, get_origin, get_args

T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self):
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return bool(self._items)


def first(items: Sequence[T]) -> T | None:
    return items[0] if items else None


def typed_deserialize(data, target_type):
    origin = get_origin(target_type)

    if origin is list:
        (item_type,) = get_args(target_type)
        return [typed_deserialize(item, item_type) for item in data]

    if target_type is str and not isinstance(data, str):
        return str(data)

    if target_type is int and isinstance(data, str):
        return int(data)

    return data
