"""Module 06: Decorators and Context Managers — Reference Implementation."""

import functools
import inspect
import time
from pathlib import Path


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timer] {func.__name__} took {elapsed:.4f}s")
        return result

    return wrapper


def retry(max_attempts=3, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == max_attempts:
                        raise
            return None

        return wrapper

    return decorator


def memoize(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper


class TimedOpen:
    def __init__(self, filepath, mode="r"):
        self.filepath = Path(filepath)
        self.mode = mode
        self._file = None
        self._start = None

    def __enter__(self):
        self._start = time.perf_counter()
        self._file = open(self.filepath, self.mode)
        return self._file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()
        elapsed = time.perf_counter() - self._start
        print(f"[TimedOpen] {self.filepath.name} open for {elapsed:.4f}s")
        return False


def validate_types(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        for name, value in bound.arguments.items():
            if name in func.__annotations__:
                expected = func.__annotations__[name]
                if not isinstance(value, expected):
                    raise TypeError(
                        f"Argument '{name}' expected {expected.__name__}, "
                        f"got {type(value).__name__}"
                    )

        return func(*args, **kwargs)

    return wrapper
