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
    # BUG: this code has a problem. Find and fix it.
    words = text.lower().split()
    return {word: words.count(word) for word in words}


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


def create_counter(start: int = 0):
    """Return a closure that increments and returns a counter on each call.

    Uses the 'nonlocal' keyword to mutate captured state across calls.
    This bridges functional and OOP thinking — a closure captures state
    (like fields) and exposes behavior (like methods), foreshadowing classes.

    Java analogy: A lambda capturing a mutable local variable... except
    Java requires captured variables to be effectively final. Python closures
    can mutate captured variables via 'nonlocal'.

    counter = create_counter()
    counter()  # 1
    counter()  # 2
    counter2 = create_counter(10)
    counter2()  # 11
    """
    raise NotImplementedError("TODO: implement create_counter")
