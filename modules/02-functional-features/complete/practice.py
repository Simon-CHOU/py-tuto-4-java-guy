"""Module 02: Functional Features — Reference Implementation."""

import re
import string


def select_and_transform(items, predicate, transform):
    return [transform(x) for x in items if predicate(x)]


def word_frequencies(text):
    cleaned = re.sub(rf"[{re.escape(string.punctuation)}]", "", text).lower()
    words = cleaned.split()
    return {word: words.count(word) for word in set(words)}


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def group_by(iterable, key_func):
    result = {}
    for item in iterable:
        key = key_func(item)
        result.setdefault(key, []).append(item)
    return result


def running_average(iterable):
    total = 0
    for i, value in enumerate(iterable, start=1):
        total += value
        yield total / i


def interleave(*iterables):
    iterators = [iter(it) for it in iterables]
    while iterators:
        exhausted = []
        for it in iterators:
            try:
                yield next(it)
            except StopIteration:
                exhausted.append(it)
        for it in exhausted:
            iterators.remove(it)
        if not iterators:
            break


def create_counter(start: int = 0):
    """Return a closure that increments and returns a counter on each call.

    This PREVIEWS state + behavior — the core of OOP — using only functions.
    The closure captures `count` (state) and exposes `increment` (behavior).
    'nonlocal' is Python's way of saying "this variable belongs to the enclosing scope."
    """
    count = start

    def increment():
        nonlocal count
        count += 1
        return count

    return increment
