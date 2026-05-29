"""Module 04: Interfaces and Abstraction — Your Implementation."""


# TODO: import ABC, abstractmethod from abc
# TODO: import OrderedDict from collections
# TODO: import Path from pathlib

class DataStore:
    """Abstract base class defining the contract for a key-value store.

    Java analogy:
        public interface DataStore<V> {
            V get(String key);
            void set(String key, V value);
            void delete(String key);
        }

    In Python, use ABC (Abstract Base Class) + @abstractmethod.
    Trying to instantiate DataStore() should raise TypeError.
    """
    raise NotImplementedError("TODO: implement DataStore as an ABC")


class DictStore(DataStore):
    """Simple dict-backed implementation of DataStore. Extends DataStore."""
    raise NotImplementedError("TODO: implement DictStore")


class LRUStore(DataStore):
    """LRU eviction key-value store. Extends DataStore.

    Use collections.OrderedDict — it remembers insertion order
    and has move_to_end().
    """
    raise NotImplementedError("TODO: implement LRUStore")


def save_to_file(obj, filepath):
    """Save an object to file if it has a to_json() method.

    This demonstrates DUCK TYPING — no interface needed.
    Any object with to_json() works. Use hasattr() to check.

    Java analogy: Collections.sort() works on any List<T> where T implements Comparable.
    Python doesn't check at compile time — it just calls the method at runtime.
    """
    raise NotImplementedError("TODO: implement save_to_file")
