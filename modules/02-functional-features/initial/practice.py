"""Module 02: Functional Features — Your Implementation."""


def select_and_transform(items, predicate, transform):
    """Filter items by predicate, apply transform, return a new list. Use a list comprehension.

    Java analogy: items.stream().filter(predicate).map(transform).collect(toList())
    Python:       [transform(x) for x in items if predicate(x)]
    """
    raise NotImplementedError("TODO: implement select_and_transform")


def word_frequencies(text):
    """Return a dict mapping each word to its count. Case-insensitive, ignore punctuation.

    Use a dict comprehension: {key: value for item in iterable}
    Or use collections.Counter from the standard library.
    """
    raise NotImplementedError("TODO: implement word_frequencies")


def fibonacci():
    """Generator yielding the Fibonacci sequence indefinitely.

    Python has no 'yield' in Java. 'yield' turns a function into a generator:
    values are produced lazily, one at a time, on demand.

    Use tuple unpacking: a, b = b, a + b
    """
    raise NotImplementedError("TODO: implement fibonacci")


def group_by(iterable, key_func):
    """Group elements by key_func, returning a dict of key -> list of values.

    Java: Collectors.groupingBy(keyFunc)
    Python: use a plain dict with setdefault() or defaultdict(list)
    """
    raise NotImplementedError("TODO: implement group_by")


def running_average(iterable):
    """Generator yielding the cumulative average as each element is consumed.

    Use yield in a loop. Keep a running total and count.
    """
    raise NotImplementedError("TODO: implement running_average")


def interleave(*iterables):
    """Generator that interleaves elements from multiple iterables. Exhausts all iterables.

    Example: interleave([1, 2], ['a', 'b', 'c']) -> 1, 'a', 2, 'b', 'c'

    *iterables means the function accepts any number of arguments (varargs).
    Use iter() to create iterators, next() to get values, catch StopIteration.
    """
    raise NotImplementedError("TODO: implement interleave")
