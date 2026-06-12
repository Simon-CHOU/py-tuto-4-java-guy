"""Module 04: Interfaces and Abstraction — Reference Implementation."""

from abc import ABC, abstractmethod
from collections import OrderedDict
from pathlib import Path


class DataStore(ABC):
    @abstractmethod
    def get(self, key): ...

    @abstractmethod
    def set(self, key, value): ...

    @abstractmethod
    def delete(self, key): ...


class DictStore(DataStore):
    def __init__(self):
        self._data = {}

    def get(self, key):
        if key not in self._data:
            raise KeyError(key)
        return self._data[key]

    def set(self, key, value):
        self._data[key] = value

    def delete(self, key):
        if key not in self._data:
            raise KeyError(key)
        del self._data[key]


class LRUStore(DataStore):
    def __init__(self, capacity):
        self._capacity = capacity
        self._data = OrderedDict()

    def get(self, key):
        if key not in self._data:
            raise KeyError(key)
        self._data.move_to_end(key)
        return self._data[key]

    def set(self, key, value):
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self._capacity:
            self._data.popitem(last=False)

    def delete(self, key):
        if key not in self._data:
            raise KeyError(key)
        del self._data[key]


def save_to_file(obj, filepath):
    if not hasattr(obj, "to_json") or not callable(obj.to_json):
        raise TypeError(f"Object of type {type(obj).__name__} has no to_json() method")
    data = obj.to_json()
    Path(filepath).write_text(data)
