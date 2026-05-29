# Python Tutorial for Java Devs — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an 8-module interactive Python tutorial teaching Java developers Python through comparison-based Jupyter notebooks and TDD code exercises.

**Architecture:** Each module is a self-contained directory with identical structure: `tutorial.ipynb` (6-section Jupyter notebook), `initial/practice.py` (skeleton with `NotImplementedError`), `complete/practice.py` (reference implementation), `test_practice.py` (shared pytest suite), and `run_test.py` (cross-platform test runner). All tutorial code is stdlib-only. Tooling uses uv + pytest + jupyter.

**Tech Stack:** Python 3.12+, uv, pytest, jupyter (nbformat for programmatic notebook creation)

---

### Task 1: Project Scaffolding

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `modules/__init__.py`

- [ ] **Step 1: Create pyproject.toml**

```toml
[project]
name = "py-tuto-4-java-guy"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "jupyter>=1.0",
    "nbformat>=5.0",
]

[tool.pytest.ini_options]
testpaths = ["modules"]
```

- [ ] **Step 2: Create .gitignore**

```
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.pytest_cache/
*.egg-info/
```

- [ ] **Step 3: Create directories and empty files**

```bash
mkdir -p modules
mkdir -p modules/01-basics-and-types/initial
mkdir -p modules/01-basics-and-types/complete
mkdir -p modules/02-functional-features/initial
mkdir -p modules/02-functional-features/complete
mkdir -p modules/03-oop/initial
mkdir -p modules/03-oop/complete
mkdir -p modules/04-interfaces-and-abstraction/initial
mkdir -p modules/04-interfaces-and-abstraction/complete
mkdir -p modules/05-modules-and-packages/initial
mkdir -p modules/05-modules-and-packages/complete
mkdir -p modules/06-decorators-and-context-managers/initial
mkdir -p modules/06-decorators-and-context-managers/complete
mkdir -p modules/07-type-hints/initial
mkdir -p modules/07-type-hints/complete
mkdir -p modules/08-concurrency-and-parallelism/initial
mkdir -p modules/08-concurrency-and-parallelism/complete
touch modules/__init__.py
```

- [ ] **Step 4: Set up uv environment**

```bash
uv python install 3.14
uv venv
uv pip install -e ".[dev]"
```

- [ ] **Step 5: Verify pytest works**

```bash
pytest --version
```
Expected: `pytest 8.x.x`

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml .gitignore modules/__init__.py
git commit -m "chore: scaffold project with uv + pytest"
```

---

### Task 2: Module 01 — Basics and Types (test_practice.py)

**Files:**
- Create: `modules/01-basics-and-types/test_practice.py`

- [ ] **Step 1: Write test_practice.py**

```python
"""Tests for Module 01: Basics and Types."""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

import pytest
from practice import (
    classify_number,
    safe_divide,
    format_table,
    is_palindrome,
    flatten_nested,
    merge_defaults,
)


class TestClassifyNumber:
    def test_positive_even(self):
        assert classify_number(4) == "positive even"

    def test_positive_odd(self):
        assert classify_number(7) == "positive odd"

    def test_negative_even(self):
        assert classify_number(-6) == "negative even"

    def test_negative_odd(self):
        assert classify_number(-3) == "negative odd"

    def test_zero(self):
        assert classify_number(0) == "zero even"

    def test_type_error_on_float(self):
        with pytest.raises(TypeError):
            classify_number(3.14)

    def test_type_error_on_str(self):
        with pytest.raises(TypeError):
            classify_number("42")


class TestSafeDivide:
    def test_normal_division(self):
        assert safe_divide(10, 3) == (3, 1)

    def test_exact_division(self):
        assert safe_divide(10, 2) == (5, 0)

    def test_division_by_zero(self):
        with pytest.raises(ValueError, match="zero"):
            safe_divide(5, 0)

    def test_negative_dividend(self):
        assert safe_divide(-10, 3) == (-4, 2)

    def test_both_negative(self):
        assert safe_divide(-10, -3) == (3, -1)


class TestFormatTable:
    def test_basic_table(self):
        data = [
            {"name": "Alice", "score": 95},
            {"name": "Bob", "score": 87},
        ]
        result = format_table(data)
        assert "Alice" in result
        assert "95" in result
        assert "Bob" in result
        assert "87" in result

    def test_empty_list(self):
        assert format_table([]) == ""

    def test_single_row(self):
        data = [{"name": "Alice", "score": 95}]
        result = format_table(data)
        assert "Alice" in result
        assert "95" in result


class TestIsPalindrome:
    def test_simple_palindrome(self):
        assert is_palindrome("racecar") is True

    def test_not_palindrome(self):
        assert is_palindrome("hello") is False

    def test_ignore_case_and_spaces(self):
        assert is_palindrome("A man a plan a canal Panama") is True

    def test_ignore_punctuation(self):
        assert is_palindrome("Was it a car or a cat I saw?") is True

    def test_empty_string(self):
        assert is_palindrome("") is True

    def test_single_char(self):
        assert is_palindrome("a") is True


class TestFlattenNested:
    def test_already_flat(self):
        assert flatten_nested([1, 2, 3]) == [1, 2, 3]

    def test_one_level(self):
        assert flatten_nested([1, [2, 3], 4]) == [1, 2, 3, 4]

    def test_deeply_nested(self):
        assert flatten_nested([1, [2, [3, [4]]]]) == [1, 2, 3, 4]

    def test_empty_list(self):
        assert flatten_nested([]) == []

    def test_mixed_empty_sublists(self):
        assert flatten_nested([1, [], [2, []]]) == [1, 2]


class TestMergeDefaults:
    def test_merge_overrides(self):
        defaults = {"a": 1, "b": 2}
        overrides = {"b": 3, "c": 4}
        result = merge_defaults(defaults, overrides)
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_defaults_not_mutated(self):
        defaults = {"a": 1}
        overrides = {"a": 2, "b": 3}
        merge_defaults(defaults, overrides)
        assert defaults == {"a": 1}

    def test_no_overrides(self):
        defaults = {"a": 1, "b": 2}
        result = merge_defaults(defaults, {})
        assert result == {"a": 1, "b": 2}
        assert result is not defaults  # new dict, not same reference
```

- [ ] **Step 2: Commit**

```bash
git add modules/01-basics-and-types/test_practice.py
git commit -m "test(01): add test suite for basics and types"
```

---

### Task 3: Module 01 — Basics and Types (complete/practice.py)

**Files:**
- Create: `modules/01-basics-and-types/complete/practice.py`

- [ ] **Step 1: Write complete/practice.py**

```python
"""Module 01: Basics and Types — Reference Implementation."""

import re
import string


def classify_number(n):
    """Return a string describing whether n is positive/negative/zero and even/odd."""
    if not isinstance(n, int):
        raise TypeError(f"Expected int, got {type(n).__name__}")
    sign = "positive" if n > 0 else ("negative" if n < 0 else "zero")
    parity = "even" if n % 2 == 0 else "odd"
    return f"{sign} {parity}"


def safe_divide(a, b):
    """Return (quotient, remainder) for a // b. Raise ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return (a // b, a % b)


def format_table(rows):
    """Given a list of dicts with the same keys, return a formatted ASCII table string."""
    if not rows:
        return ""
    keys = list(rows[0].keys())
    col_widths = {
        key: max(len(str(key)), max(len(str(row.get(key, ""))) for row in rows))
        for key in keys
    }
    header = " | ".join(str(key).ljust(col_widths[key]) for key in keys)
    separator = "-+-".join("-" * col_widths[key] for key in keys)
    body = "\n".join(
        " | ".join(str(row.get(key, "")).ljust(col_widths[key]) for key in keys)
        for row in rows
    )
    return f"{header}\n{separator}\n{body}"


def is_palindrome(s):
    """Return True if s is a palindrome, ignoring case, whitespace, and punctuation."""
    cleaned = re.sub(rf"[{re.escape(string.punctuation)}\s]", "", s).lower()
    return cleaned == cleaned[::-1]


def flatten_nested(nested):
    """Recursively flatten an arbitrarily nested list. Return a new flat list."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten_nested(item))
        else:
            result.append(item)
    return result


def merge_defaults(defaults, overrides):
    """Return a new dict merging defaults with overrides, without mutating inputs."""
    return {**defaults, **overrides}
```

- [ ] **Step 2: Create run_test.py for module 01**

```python
"""Run tests for module 01 against initial/ or complete/ implementation."""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("initial", "complete"):
        print("Usage: python run_test.py initial|complete", file=sys.stderr)
        sys.exit(1)

    env = {**os.environ, "PRACTICE_TARGET": sys.argv[1]}
    args = [sys.executable, "-m", "pytest", str(HERE / "test_practice.py"), "-v"]
    result = subprocess.run(args, env=env, cwd=str(HERE))
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Verify complete passes tests**

```bash
cd modules/01-basics-and-types && python run_test.py complete
```
Expected: 22 passed

- [ ] **Step 4: Commit**

```bash
git add modules/01-basics-and-types/complete/practice.py modules/01-basics-and-types/run_test.py
git commit -m "feat(01): add complete reference implementation for basics and types"
```

---

### Task 4: Module 01 — Basics and Types (initial/practice.py + tutorial.ipynb)

**Files:**
- Create: `modules/01-basics-and-types/initial/practice.py`
- Create: `modules/01-basics-and-types/tutorial.ipynb`

- [ ] **Step 1: Write initial/practice.py (skeleton)**

```python
"""Module 01: Basics and Types — Your Implementation."""


def classify_number(n):
    """Return a string describing whether n is positive/negative/zero and even/odd.

    Examples:
        classify_number(4)  -> "positive even"
        classify_number(-3) -> "negative odd"
        classify_number(0)  -> "zero even"
    Raises TypeError for non-int input.
    """
    raise NotImplementedError("TODO: implement classify_number")


def safe_divide(a, b):
    """Return (quotient, remainder) for a // b. Raise ValueError if b is zero.

    Python uses // for floor division and % for modulo. Together they satisfy:
        a = b * (a // b) + (a % b)

    The remainder always has the same sign as the divisor.
    """
    raise NotImplementedError("TODO: implement safe_divide")


def format_table(rows):
    """Given a list of dicts with the same keys, return a formatted ASCII table string.

    Example:
        format_table([{"name": "Alice", "score": 95}]) ->
        "name  | score\n------+------\nAlice | 95"

    Python's f-strings and str.ljust()/rjust()/center() are your friends here.
    """
    raise NotImplementedError("TODO: implement format_table")


def is_palindrome(s):
    """Return True if s is a palindrome, ignoring case, whitespace, and punctuation.

    Python strings support slicing with step: s[::-1] returns the reversed string.
    Use str.lower(), str.isalnum(), or re.sub() from the re module.
    """
    raise NotImplementedError("TODO: implement is_palindrome")


def flatten_nested(nested):
    """Recursively flatten an arbitrarily nested list. Return a new flat list.

    Example:
        flatten_nested([1, [2, [3, [4]]]]) -> [1, 2, 3, 4]

    isinstance(item, list) is the Python way to check if something is a list.
    """
    raise NotImplementedError("TODO: implement flatten_nested")


def merge_defaults(defaults, overrides):
    """Return a new dict merging defaults with overrides, without mutating inputs.

    Example:
        merge_defaults({"a": 1, "b": 2}, {"b": 3, "c": 4}) -> {"a": 1, "b": 3, "c": 4}

    Python's {**d1, **d2} syntax merges two dicts into a new one. Keys in d2 override d1.
    This is the Python idiom for "copy with updates" — no need for a builder pattern.
    """
    raise NotImplementedError("TODO: implement merge_defaults")
```

- [ ] **Step 2: Verify initial fails (expected behavior)**

```bash
cd modules/01-basics-and-types && python run_test.py initial
```
Expected: All 22 tests FAIL (NotImplementedError)

- [ ] **Step 3: Write tutorial.ipynb using nbformat**

```bash
python -c "
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}

nb.cells = [
    nbf.v4.new_markdown_cell('''# Module 01: Python Basics and Types for Java Developers

## Java Recall

In Java, you are used to:

```java
int x = 42;           // primitive — not an object
String s = \"hello\";   // reference type — IS an object
boolean b = true;      // primitive
Integer boxed = x;     // autoboxing wraps primitive into object

// Type checking at compile time
if (x instanceof Integer) { }  // won't compile — x is int, not a reference type
```

Every type is either a primitive or a reference type. Primitives live on the stack, objects on the heap. The compiler checks types before your code ever runs.'''),

    nbf.v4.new_markdown_cell('''## Python Way

```python
x = 42                # Everything is an object — yes, even integers
s = \"hello\"           # str object
b = True              # bool is a subclass of int (True == 1, False == 0)

# Type checking at runtime
print(type(x))        # <class 'int'>
print(isinstance(x, int))  # True
print(isinstance(x, object))  # True — int inherits from object

# Dynamic typing — variables don't have types, values do
x = 42
x = \"now I'm a string\"  # perfectly valid
```

**Key insight:** In Python, `int` is a class. `42` is an instance of `int`. There are no primitives. The variable name `x` is just a label — it has no type, only the object it points to has a type.'''),

    nbf.v4.new_markdown_cell('''## Key Differences

| Concept | Java | Python |
|---------|------|--------|
| Type system | Static, compile-time | Dynamic, runtime (\"duck typing\") |
| Primitives | Yes (int, boolean, char...) | No — everything is an object |
| `null` | `null` (only for reference types) | `None` (singleton object, has type `NoneType`) |
| Type checking | `x instanceof String` | `isinstance(x, str)` |
| String format | `String.format()` / `+` | f-strings: `f\"Hello {name}\"` |
| Switch/case | `switch` expression (Java 14+) | `match/case` (Python 3.10+) |
| Division | `/` with ints truncates | `/` always returns float, `//` for floor division |
| Boolean | `boolean` primitive | `bool` subclass of `int` (True==1, False==0) |

**The \"everything is an object\" design** means Python has no unboxed primitives. This makes the language simpler but has performance implications — Python uses reference counting and garbage collection for ALL values, including integers. Small integers (-5 to 256) are cached as a CPython optimization.'''),

    nbf.v4.new_markdown_cell('''## Pitfalls and Interview Traps

### 1. Mutable default arguments
```python
def append_to(item, target=[]):  # DANGER: [] is created ONCE at function definition
    target.append(item)
    return target

>>> append_to(1)
[1]
>>> append_to(2)
[1, 2]  # WTF?! The same list object was reused!
```
**Fix:** `def append_to(item, target=None): if target is None: target = []`

### 2. `is` vs `==`
```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b  # True — same value
a is b  # False — different objects in memory
```
`is` checks identity (same object), `==` checks equality (same value). Think `==` vs `.equals()` in Java.

### 3. Truthiness
```python
# These are ALL falsy in Python:
bool(0), bool(0.0), bool(\"\"), bool([]), bool({}), bool(None), bool(False)
# Everything else is truthy — including \"False\", [False], etc.
```

### 4. Integer caching surprise
```python
a = 256
b = 256
a is b  # True — cached!

a = 257
b = 257
a is b  # False (usually) — not cached
```
CPython caches integers -5 to 256. Don't rely on `is` for integer comparison — use `==`.'''),

    nbf.v4.new_markdown_cell('''## Your Practice

Open `initial/practice.py`. You'll find 6 functions to implement:

1. **classify_number** — Dynamic typing, control flow
2. **safe_divide** — Integer division, exceptions
3. **format_table** — String formatting, f-strings
4. **is_palindrome** — String manipulation, regex
5. **flatten_nested** — Recursion, isinstance
6. **merge_defaults** — Dict operations, immutability

Run the tests:
```bash
cd modules/01-basics-and-types
python run_test.py initial    # Your code (starts failing)
python run_test.py complete   # Reference answer (passes)
```

Check `complete/practice.py` after you finish to compare implementations.'''),

    nbf.v4.new_markdown_cell('''## References

- [Python Built-in Types](https://docs.python.org/3/library/stdtypes.html)
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
- [f-strings PEP 498](https://peps.python.org/pep-0498/)
'''),
]

nbf.write(nb, 'modules/01-basics-and-types/tutorial.ipynb')
"
```

- [ ] **Step 4: Verify final state**

```bash
cd modules/01-basics-and-types && python run_test.py initial 2>&1 | head -5
# Expected: FAILED (errors due to NotImplementedError)
cd modules/01-basics-and-types && python run_test.py complete 2>&1 | tail -3
# Expected: 22 passed
```

- [ ] **Step 5: Commit**

```bash
git add modules/01-basics-and-types/
git commit -m "feat(01): add initial skeleton and tutorial notebook"
```

---

### Task 5: Module 02 — Functional Features (test_practice.py)

**Files:**
- Create: `modules/02-functional-features/test_practice.py`

- [ ] **Step 1: Write test_practice.py**

```python
"""Tests for Module 02: Functional Features."""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

import pytest
from practice import (
    select_and_transform,
    word_frequencies,
    fibonacci,
    group_by,
    running_average,
    interleave,
)


class TestSelectAndTransform:
    def test_filter_and_square(self):
        result = select_and_transform(
            [1, 2, 3, 4, 5, 6],
            predicate=lambda x: x > 3,
            transform=lambda x: x ** 2,
        )
        assert result == [16, 25, 36]

    def test_all_pass(self):
        assert select_and_transform([1, 2, 3], lambda x: True, lambda x: x * 2) == [2, 4, 6]

    def test_none_pass(self):
        assert select_and_transform([1, 2, 3], lambda x: x > 10, lambda x: x * 2) == []

    def test_returns_list_not_generator(self):
        result = select_and_transform([1, 2], lambda x: True, lambda x: x)
        assert isinstance(result, list)


class TestWordFrequencies:
    def test_simple(self):
        result = word_frequencies("hello world hello")
        assert result == {"hello": 2, "world": 1}

    def test_case_insensitive(self):
        result = word_frequencies("Hello hello HELLO")
        assert result == {"hello": 3}

    def test_ignores_punctuation(self):
        result = word_frequencies("hello! world? hello.")
        assert result == {"hello": 2, "world": 1}

    def test_empty_string(self):
        assert word_frequencies("") == {}


class TestFibonacci:
    def test_first_ten(self):
        gen = fibonacci()
        first_ten = [next(gen) for _ in range(10)]
        assert first_ten == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_is_generator(self):
        import types
        assert isinstance(fibonacci(), types.GeneratorType)


class TestGroupBy:
    def test_by_length(self):
        words = ["cat", "dog", "bird", "fish", "elephant"]
        result = group_by(words, len)
        assert result == {3: ["cat", "dog"], 4: ["bird", "fish"], 8: ["elephant"]}

    def test_by_first_letter(self):
        words = ["apple", "ant", "banana", "bat"]
        result = group_by(words, lambda w: w[0])
        assert result == {"a": ["apple", "ant"], "b": ["banana", "bat"]}

    def test_empty_list(self):
        assert group_by([], len) == {}


class TestRunningAverage:
    def test_sequence(self):
        result = list(running_average([2, 4, 6, 8]))
        assert result == [2.0, 3.0, 4.0, 5.0]

    def test_single_element(self):
        assert list(running_average([42])) == [42.0]

    def test_empty(self):
        assert list(running_average([])) == []

    def test_is_generator(self):
        import types
        assert isinstance(running_average([1]), types.GeneratorType)


class TestInterleave:
    def test_two_lists(self):
        result = list(interleave([1, 2, 3], ["a", "b", "c"]))
        assert result == [1, "a", 2, "b", 3, "c"]

    def test_unequal_lengths(self):
        result = list(interleave([1, 2, 3, 4], ["a"]))
        assert result == [1, "a", 2, 3, 4]

    def test_empty_iterable(self):
        result = list(interleave([], [1, 2, 3]))
        assert result == [1, 2, 3]

    def test_is_generator(self):
        import types
        assert isinstance(interleave([1], [2]), types.GeneratorType)
```

- [ ] **Step 2: Commit**

```bash
git add modules/02-functional-features/test_practice.py
git commit -m "test(02): add test suite for functional features"
```

---

### Task 6: Module 02 — Functional Features (complete + initial + notebook)

**Files:**
- Create: `modules/02-functional-features/complete/practice.py`
- Create: `modules/02-functional-features/initial/practice.py`
- Create: `modules/02-functional-features/run_test.py`
- Create: `modules/02-functional-features/tutorial.ipynb`

- [ ] **Step 1: Write complete/practice.py**

```python
"""Module 02: Functional Features — Reference Implementation."""

import itertools
import re
import string


def select_and_transform(items, predicate, transform):
    """Filter items by predicate, apply transform, return a new list. Use a list comprehension."""
    return [transform(x) for x in items if predicate(x)]


def word_frequencies(text):
    """Return a dict mapping each word to its count. Case-insensitive, ignore punctuation. Use a dict comprehension."""
    cleaned = re.sub(rf"[{re.escape(string.punctuation)}]", "", text).lower()
    words = cleaned.split()
    return {word: words.count(word) for word in set(words)}


def fibonacci():
    """Generator yielding the Fibonacci sequence indefinitely (0, 1, 1, 2, 3, 5, ...)."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def group_by(iterable, key_func):
    """Group elements by key_func, returning a dict of key -> list of values."""
    result = {}
    for item in iterable:
        key = key_func(item)
        result.setdefault(key, []).append(item)
    return result


def running_average(iterable):
    """Generator yielding the cumulative average as each element is consumed."""
    total = 0
    for i, value in enumerate(iterable, start=1):
        total += value
        yield total / i


def interleave(*iterables):
    """Generator that interleaves elements from multiple iterables. Exhausts all iterables."""
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
```

- [ ] **Step 2: Write initial/practice.py**

```python
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
```

- [ ] **Step 3: Create run_test.py**

Copy `modules/01-basics-and-types/run_test.py` to `modules/02-functional-features/run_test.py`.

- [ ] **Step 4: Create tutorial.ipynb**

```bash
python -c "
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}

nb.cells = [
    nbf.v4.new_markdown_cell('''# Module 02: Functional Features for Java Developers

## Java Recall

Java's Stream API brought functional programming to Java:

```java
var result = items.stream()
    .filter(x -> x > 3)
    .map(x -> x * x)
    .collect(Collectors.toList());

// Infinite sequences require custom Spliterator
// Lazy evaluation with streams
```

Java lambdas implement functional interfaces (SAM types). Streams are lazy — nothing happens until a terminal operation like `.collect()` or `.forEach()`.'''),

    nbf.v4.new_markdown_cell('''## Python Way

```python
# List comprehension — the Pythonic way to filter + map
result = [x ** 2 for x in items if x > 3]

# Dict comprehension
freq = {w: words.count(w) for w in set(words)}

# Generator expression — lazy, like a Stream
squares = (x ** 2 for x in range(10**9))  # No memory allocated yet

# Generator function — yields values one at a time
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

**Critical difference:** Python's `lambda` is restricted to a SINGLE expression. No statements, no multiple lines. If your logic is complex, use a named `def` — it's more readable and more Pythonic.'''),

    nbf.v4.new_markdown_cell('''## Key Differences

| Concept | Java | Python |
|---------|------|--------|
| Filter + map | `.stream().filter().map().collect()` | List comprehension: `[f(x) for x in seq if p(x)]` |
| Lambda | Multi-line with `{}` | Single expression only |
| Lazy sequence | `Stream<T>` | Generator expression or `yield` |
| Group by | `Collectors.groupingBy()` | Loop + `dict.setdefault()` or `itertools.groupby()` |
| Reduce | `.reduce()` | `functools.reduce()` (use sparingly) |
| Method reference | `String::length` | `len` (function, not method — no `::`) |
| Infinite stream | `Stream.iterate()` | `while True: yield ...` |
| First-class functions | No — lambdas are syntax sugar for functional interfaces | Yes — functions are objects |'''),

    nbf.v4.new_markdown_cell('''## Pitfalls and Interview Traps

### 1. Comprehensions leak the loop variable (fixed in Python 3)
```python
[x for x in range(3)]
print(x)  # Python 2: 2 (leaked!), Python 3: NameError (fixed)
```

### 2. Generator expressions are lazy — consume once
```python
gen = (x ** 2 for x in range(5))
list(gen)  # [0, 1, 4, 9, 16]
list(gen)  # [] — already exhausted!
```
A generator is like a one-pass Iterator, not a reusable Stream.

### 3. `lambda` limitations
Can't use `lambda` when you need:
- Multiple statements
- Assignment (`=`)
- `return`, `try`, `with`, `for`, `while`

Just use `def`. A nested `def` inside another function is perfectly Pythonic.

### 4. Avoid `map`/`filter` with lambda — use comprehensions
```python
# Readable:
[x ** 2 for x in numbers if x > 0]

# Noisy:
list(map(lambda x: x ** 2, filter(lambda x: x > 0, numbers)))
```
Python's creator (Guido) wanted to remove `map`/`filter`/`reduce` from the language. Comprehensions are the preferred style.'''),

    nbf.v4.new_markdown_cell('''## Your Practice

Open `initial/practice.py`. You'll implement:

1. **select_and_transform** — List comprehension (Java's filter+map)
2. **word_frequencies** — Dict comprehension + string cleaning
3. **fibonacci** — Infinite generator with `yield`
4. **group_by** — Group by key (Java's groupingBy)
5. **running_average** — Stateful generator
6. **interleave** — Multi-iterator generator

Run: `python run_test.py initial` to test your work, `python run_test.py complete` for comparison.'''),

    nbf.v4.new_markdown_cell('''## References

- [Python List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [Python Generators](https://docs.python.org/3/tutorial/classes.html#generators)
- [itertools — Functions creating iterators](https://docs.python.org/3/library/itertools.html)
'''),
]

nbf.write(nb, 'modules/02-functional-features/tutorial.ipynb')
"
```

- [ ] **Step 5: Verify**

```bash
cd modules/02-functional-features && python run_test.py complete
```
Expected: 14 passed

- [ ] **Step 6: Commit**

```bash
git add modules/02-functional-features/
git commit -m "feat(02): add functional features module (complete + initial + notebook)"
```

---

### Task 7: Module 03 — Object-Oriented Programming

**Files:**
- Create: `modules/03-oop/test_practice.py`
- Create: `modules/03-oop/complete/practice.py`
- Create: `modules/03-oop/initial/practice.py`
- Create: `modules/03-oop/run_test.py`
- Create: `modules/03-oop/tutorial.ipynb`

- [ ] **Step 1: Write test_practice.py**

```python
"""Tests for Module 03: Object-Oriented Programming."""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

import math
import pytest
from practice import Vector2D, BetterDict, Temperature, ImmutableConfig


class TestVector2D:
    def test_init_and_repr(self):
        v = Vector2D(3, 4)
        assert repr(v) == "Vector2D(3, 4)"

    def test_equality(self):
        assert Vector2D(1, 2) == Vector2D(1, 2)
        assert Vector2D(1, 2) != Vector2D(3, 4)
        assert Vector2D(1, 2) != "not a vector"

    def test_add(self):
        v1 = Vector2D(1, 2)
        v2 = Vector2D(3, 4)
        assert v1 + v2 == Vector2D(4, 6)

    def test_sub(self):
        v1 = Vector2D(5, 7)
        v2 = Vector2D(2, 3)
        assert v1 - v2 == Vector2D(3, 4)

    def test_abs(self):
        v = Vector2D(3, 4)
        assert abs(v) == 5.0

    def test_bool(self):
        assert bool(Vector2D(1, 0)) is True
        assert bool(Vector2D(0, 0)) is False

    def test_immutable(self):
        v = Vector2D(1, 2)
        with pytest.raises(AttributeError):
            v.x = 5


class TestBetterDict:
    def test_dot_access(self):
        d = BetterDict({"name": "Alice", "age": 30})
        assert d.name == "Alice"
        assert d.age == 30

    def test_key_fallback(self):
        d = BetterDict({"name": "Alice"})
        assert d["name"] == "Alice"

    def test_missing_attribute(self):
        d = BetterDict({"name": "Alice"})
        with pytest.raises(AttributeError):
            _ = d.nonexistent


class TestTemperature:
    def test_celsius_getter(self):
        t = Temperature(celsius=0)
        assert t.celsius == 0

    def test_fahrenheit_getter(self):
        t = Temperature(celsius=0)
        assert t.fahrenheit == 32.0

    def test_fahrenheit_setter(self):
        t = Temperature(celsius=0)
        t.fahrenheit = 212
        assert t.celsius == 100.0

    def test_celsius_setter(self):
        t = Temperature(celsius=0)
        t.celsius = 100
        assert t.fahrenheit == 212.0


class TestImmutableConfig:
    def test_init_with_kwargs(self):
        c = ImmutableConfig(host="localhost", port=8080)
        assert c.host == "localhost"
        assert c.port == 8080

    def test_prevent_mutation(self):
        c = ImmutableConfig(host="localhost")
        with pytest.raises(AttributeError):
            c.host = "other"

    def test_prevent_new_attr(self):
        c = ImmutableConfig(host="localhost")
        with pytest.raises(AttributeError):
            c.new_attr = 42
```

- [ ] **Step 2: Write complete/practice.py**

```python
"""Module 03: OOP — Reference Implementation."""

import math


class Vector2D:
    """Immutable 2D vector with dunder methods."""
    __slots__ = ("_x", "_y")  # memory optimization + prevents __dict__

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

    def __setattr__(self, name, value):
        raise AttributeError("Vector2D is immutable")


class BetterDict(dict):
    """A dict subclass that allows attribute-style access (d.key in addition to d['key'])."""
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
    """A configuration object that freezes after __init__. Uses __setattr__ to prevent changes."""
    __slots__ = tuple()  # Overridden in __init__ via object.__setattr__

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    def __setattr__(self, name, value):
        raise AttributeError(f"Cannot modify attribute '{name}' — object is immutable")

    def __repr__(self):
        items = {k: v for k, v in self.__dict__.items()}
        return f"ImmutableConfig({items})"
```

- [ ] **Step 3: Write initial/practice.py**

```python
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
    """A dict subclass that allows attribute-style access.

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
```

- [ ] **Step 4: Create run_test.py** — copy from Module 01

- [ ] **Step 5: Create tutorial.ipynb**

```bash
python -c "
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}

nb.cells = [
    nbf.v4.new_markdown_cell('''# Module 03: Object-Oriented Programming for Java Developers

## Java Recall

```java
public class Vector {
    private final double x;
    private final double y;

    public Vector(double x, double y) { this.x = x; this.y = y; }
    public double getX() { return x; }
    public double getY() { return y; }

    @Override
    public boolean equals(Object o) { /* ... */ }
    @Override
    public int hashCode() { /* ... */ }
    @Override
    public String toString() { return \"Vector(\" + x + \", \" + y + \")\"; }

    public Vector add(Vector other) { return new Vector(x + other.x, y + other.y); }
}
```

In Java: private fields, public getters, explicit equals/hashCode/toString, method overloading.'''),

    nbf.v4.new_markdown_cell('''## Python Way

```python
class Vector2D:
    __slots__ = ('_x', '_y')  # Like declaring fields (avoids __dict__ overhead)

    def __init__(self, x, y):
        self._x = x
        self._y = y

    # Properties replace getters — no getX() needed
    @property
    def x(self): return self._x

    # Dunder methods hook into Python language syntax
    def __repr__(self): return f\"Vector2D({self.x}, {self.y})\"
    def __eq__(self, other): return isinstance(other, Vector2D) and self.x == other.x and self.y == other.y
    def __add__(self, other): return Vector2D(self.x + other.x, self.y + other.y)
    def __abs__(self): return math.hypot(self.x, self.y)   # abs(v)
    def __bool__(self): return self.x != 0 or self.y != 0  # if v:
```

**No private, no overloading, no interfaces required.** Python trusts the developer.'''),

    nbf.v4.new_markdown_cell('''## Key Differences

| Concept | Java | Python |
|---------|------|--------|
| Constructor | ClassName() — special syntax | `__init__(self)` — initializer method |
| Self reference | `this` (implicit) | `self` (explicit first param) |
| Private fields | `private` keyword | Convention: prefix with `_` |
| Getters/setters | `getX()`/`setX()` | `@property` — transparent access |
| toString/equals | `@Override` methods | `__repr__`/`__str__`/`__eq__` (dunder) |
| Operator overloading | Not possible | `__add__`, `__sub__`, etc. |
| Inheritance | Single | Multiple (with MRO via C3 linearization) |
| Method overloading | Yes (same name, different params) | No — use default args or `*args` |
| Abstract class | `abstract class` | `ABC` + `@abstractmethod` |
| Interface | `interface` keyword | ABC / Protocol / duck typing |'''),

    nbf.v4.new_markdown_cell('''## Pitfalls and Interview Traps

### 1. MRO (Method Resolution Order) — the Diamond Problem
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.__mro__)  # D -> B -> C -> A -> object
```
Python uses C3 linearization. The order: child before parent, left before right. You can inspect it: `ClassName.__mro__`.

### 2. `__init__` is NOT a constructor
`__new__` creates the object, `__init__` initializes it. `__new__` is rarely overridden (mainly for singletons or immutable subclasses). In Java terms: `__new__` ≈ `new` bytecode, `__init__` ≈ constructor body.

### 3. Name mangling: `__name` convention
```python
class Foo:
    def __init__(self):
        self.__secret = 42  # Actually stored as _Foo__secret

f = Foo()
f.__secret  # AttributeError!
f._Foo__secret  # 42 — still accessible, just renamed
```
NOT true privacy. It's a convention to avoid name clashes in subclasses. Python's philosophy: \"We're all consenting adults.\"

### 4. Multiple inheritance and `super()`
`super()` in Python doesn't just call the parent — it follows the MRO chain. With multiple inheritance, `super()` calls the NEXT class in the MRO, not necessarily the direct parent. This is cooperative multiple inheritance.'''),

    nbf.v4.new_markdown_cell('''## Your Practice

Open `initial/practice.py`. Implement:

1. **Vector2D** — Dunder methods (__repr__, __eq__, __add__, __sub__, __abs__, __bool__)
2. **BetterDict** — Dict subclass with __getattr__ for dot access
3. **Temperature** — @property for celsius/fahrenheit conversion
4. **ImmutableConfig** — __setattr__ to prevent mutation

Run: `python run_test.py initial` to test, `python run_test.py complete` to compare.'''),

    nbf.v4.new_markdown_cell('''## References

- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
- [Descriptor Guide (properties)](https://docs.python.org/3/howto/descriptor.html)
- [MRO Documentation](https://www.python.org/download/releases/2.3/mro/)
'''),
]

nbf.write(nb, 'modules/03-oop/tutorial.ipynb')
"
```

- [ ] **Step 6: Verify and commit**

```bash
cd modules/03-oop && python run_test.py complete && git add modules/03-oop/ && git commit -m "feat(03): add OOP module (complete + initial + notebook)"
```

---

### Task 8: Module 04 — Interfaces and Abstraction

**Files:**
- Create: `modules/04-interfaces-and-abstraction/test_practice.py`
- Create: `modules/04-interfaces-and-abstraction/complete/practice.py`
- Create: `modules/04-interfaces-and-abstraction/initial/practice.py`
- Create: `modules/04-interfaces-and-abstraction/run_test.py`
- Create: `modules/04-interfaces-and-abstraction/tutorial.ipynb`

- [ ] **Step 1: Write test_practice.py**

```python
"""Tests for Module 04: Interfaces and Abstraction."""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

import json
import pytest
from practice import (
    DictStore,
    LRUStore,
    DataStore,
    save_to_file,
)


class TestDictStore:
    def test_get_set_delete(self):
        store = DictStore()
        store.set("a", 1)
        assert store.get("a") == 1
        store.delete("a")
        with pytest.raises(KeyError):
            store.get("a")

    def test_is_datastore(self):
        assert isinstance(DictStore(), DataStore)

    def test_cannot_instantiate_abc(self):
        with pytest.raises(TypeError):
            DataStore()


class TestLRUStore:
    def test_basic_operations(self):
        store = LRUStore(capacity=2)
        store.set("a", 1)
        store.set("b", 2)
        assert store.get("a") == 1
        assert store.get("b") == 2

    def test_eviction(self):
        store = LRUStore(capacity=2)
        store.set("a", 1)
        store.set("b", 2)
        store.set("c", 3)  # Evicts 'a' (least recently used)
        with pytest.raises(KeyError):
            store.get("a")
        assert store.get("b") == 2
        assert store.get("c") == 3

    def test_access_updates_lru_order(self):
        store = LRUStore(capacity=2)
        store.set("a", 1)
        store.set("b", 2)
        store.get("a")  # 'a' is now most recently used
        store.set("c", 3)  # should evict 'b'
        assert store.get("a") == 1
        with pytest.raises(KeyError):
            store.get("b")
        assert store.get("c") == 3

    def test_is_datastore(self):
        assert isinstance(LRUStore(2), DataStore)


class TestSaveToFile:
    def test_serializable(self, tmp_path):
        class User:
            def to_json(self):
                return json.dumps({"name": "Alice", "age": 30})

        filepath = tmp_path / "test.json"
        save_to_file(User(), filepath)
        saved = filepath.read_text()
        assert "Alice" in saved
        assert "30" in saved

    def test_non_serializable(self, tmp_path):
        class NoMethod:
            pass

        with pytest.raises(TypeError, match="to_json"):
            save_to_file(NoMethod(), tmp_path / "bad.json")
```

- [ ] **Step 2: Write complete/practice.py**

```python
"""Module 04: Interfaces and Abstraction — Reference Implementation."""

from abc import ABC, abstractmethod
from collections import OrderedDict
from pathlib import Path


class DataStore(ABC):
    """Abstract base class defining the contract for a key-value store.

    In Java, this would be: public interface DataStore { V get(K key); void set(K key, V value); void delete(K key); }
    """

    @abstractmethod
    def get(self, key):
        """Retrieve a value by key. Raise KeyError if not found."""
        ...

    @abstractmethod
    def set(self, key, value):
        """Store a value under the given key."""
        ...

    @abstractmethod
    def delete(self, key):
        """Remove a key and its value."""
        ...


class DictStore(DataStore):
    """Simple dict-backed implementation of DataStore."""
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
    """LRU eviction key-value store using OrderedDict."""
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
    """Save an object to file if it has a to_json() method (duck typing).

    Python doesn't need an explicit Serializable interface — any object
    with to_json() works. This is 'duck typing': if it walks like a duck...
    """
    if not hasattr(obj, "to_json") or not callable(obj.to_json):
        raise TypeError(f"Object of type {type(obj).__name__} has no to_json() method")
    data = obj.to_json()
    Path(filepath).write_text(data)
```

- [ ] **Step 3: Write initial/practice.py**

```python
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
```

- [ ] **Step 4: Create run_test.py** — copy from Module 01

- [ ] **Step 5: Create tutorial.ipynb**

```bash
python -c "
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}

nb.cells = [
    nbf.v4.new_markdown_cell('''# Module 04: Interfaces and Abstraction for Java Developers

## Interview Pro-Tip

This module covers one of the MOST COMMON interview questions for Java developers
moving to Python. The exact question: **\"Python doesn't have interfaces. How do you
express contracts and do OO design?\"**'''),

    nbf.v4.new_markdown_cell('''## Java Recall

```java
public interface DataStore {
    String get(String key);
    void set(String key, String value);
    void delete(String key);
}

public class DictStore implements DataStore {
    private Map<String, String> data = new HashMap<>();

    @Override
    public String get(String key) { return data.get(key); }

    @Override
    public void set(String key, String value) { data.put(key, value); }

    @Override
    public void delete(String key) { data.remove(key); }
}

// Compile-time enforcement: DictStore MUST implement all three methods
```

Java interfaces are contracts enforced at compile time. You can't forget a method.'''),

    nbf.v4.new_markdown_cell('''## Python Way — Three Approaches

### Approach 1: ABC (Abstract Base Class) — Most Java-like
```python
from abc import ABC, abstractmethod

class DataStore(ABC):
    @abstractmethod
    def get(self, key): ...
    @abstractmethod
    def set(self, key, value): ...
    @abstractmethod
    def delete(self, key): ...

class DictStore(DataStore):
    def get(self, key): return self._data[key]
    def set(self, key, value): self._data[key] = value
    def delete(self, key): del self._data[key]
```
- `TypeError` at instantiation if abstract methods are missing
- Runtime enforcement, not compile-time
- Supports concrete methods with default implementations (like Java default methods)

### Approach 2: Protocol (Structural Subtyping) — Modern Python (3.8+)
```python
from typing import Protocol

class DataStore(Protocol):
    def get(self, key) -> str: ...
    def set(self, key, value: str) -> None: ...
    def delete(self, key) -> None: ...

class MyStore:  # No inheritance! Just has the right methods
    def get(self, key): ...
    def set(self, key, value): ...
    def delete(self, key): ...

def process(store: DataStore):  # Type checker accepts MyStore
    store.set(\"a\", \"1\")
```
Checked by mypy, NOT at runtime. Like Go's interfaces.

### Approach 3: Duck Typing — Pure Python, No Boilerplate
```python
def save_to_file(obj, filepath):
    data = obj.to_json()  # Just call it — trust it's there
    Path(filepath).write_text(data)
```
No class hierarchy. No interface. Just call the method. This is the most \"Pythonic\" approach for simple cases. It trades compile-time safety for flexibility and less code.'''),

    nbf.v4.new_markdown_cell('''## Key Differences

| Concept | Java | Python |
|---------|------|--------|
| **Contract** | `interface` keyword | ABC + @abstractmethod OR Protocol |
| **Enforcement** | Compile-time | ABC: runtime (on instantiation) / Protocol: static checker only |
| **Multiple** | Multiple interfaces, single inheritance | Multiple inheritance (ABC + mixins) |
| **Default methods** | Java 8+ `default` keyword | Regular method on ABC (no keyword needed) |
| **Structural typing** | No (only nominal) | Protocol (structural subtyping — like Go interfaces) |
| **Duck typing** | No | Yes — the language's philosophical foundation |
| **Abstract class** | `abstract class` + `abstract method` | `ABC` + `@abstractmethod` |
| **Private methods in interface** | Java 9+ | Not applicable (convention: `_method`) |

### Which to use?

| Scenario | Recommendation |
|----------|---------------|
| Large project, Java-like discipline | ABC |
| Type-checked structural subtyping | Protocol |
| Simple utility, library code | Duck typing |
| Framework plugin system | ABC |
| Interview answer | Mention all three, explain tradeoffs |'''),

    nbf.v4.new_markdown_cell('''## Pitfalls and Interview Traps

### 1. ABC doesn't prevent instantiation if all abstract methods have implementations in a parent
```python
class Base(ABC):
    @abstractmethod
    def foo(self): ...

class Child(Base):
    def foo(self): pass  # OK now

Base()  # TypeError
Child()  # OK
```

### 2. Protocol is NOT checked at runtime
```python
class DataStore(Protocol):
    def get(self, key): ...

store = object()  # Not a DataStore
isinstance(store, DataStore)  # TypeError! Can't isinstance a Protocol at runtime (without @runtime_checkable)
```

### 3. Duck typing means runtime errors
```python
def process(obj):
    result = obj.compute()  # AttributeError at runtime if compute() doesn't exist
```
This is a tradeoff. Python values flexibility — but you trade compile-time safety.'''),

    nbf.v4.new_markdown_cell('''## Your Practice

Open `initial/practice.py`. Implement:

1. **DataStore ABC** — Define the abstract contract
2. **DictStore** — Simple dict-backed implementation
3. **LRUStore** — LRU eviction with OrderedDict
4. **save_to_file** — Duck-typing: works with any object that has to_json()

Run: `python run_test.py initial` / `python run_test.py complete`.'''),

    nbf.v4.new_markdown_cell('''## References

- [abc — Abstract Base Classes](https://docs.python.org/3/library/abc.html)
- [typing.Protocol (PEP 544)](https://peps.python.org/pep-0544/)
- [Glossary: Duck Typing](https://docs.python.org/3/glossary.html#term-duck-typing)
'''),
]

nbf.write(nb, 'modules/04-interfaces-and-abstraction/tutorial.ipynb')
"
```

- [ ] **Step 6: Verify and commit**

```bash
cd modules/04-interfaces-and-abstraction && python run_test.py complete && git add modules/04-interfaces-and-abstraction/ && git commit -m "feat(04): add interfaces and abstraction module"
```

---

### Task 9: Module 05 — Modules and Packages

**Files:**
- Create: `modules/05-modules-and-packages/test_practice.py`
- Create: `modules/05-modules-and-packages/complete/practice.py`
- Create: `modules/05-modules-and-packages/initial/practice.py`
- Create: `modules/05-modules-and-packages/run_test.py`
- Create: `modules/05-modules-and-packages/tutorial.ipynb`

- [ ] **Step 1: Write test_practice.py**

```python
"""Tests for Module 05: Modules and Packages."""
import os
import sys
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

import pytest
from practice import (
    import_from_path,
    validate_package_structure,
    detect_circular_imports,
    create_init_reexport,
)


class TestImportFromPath:
    def test_import_function(self):
        # Create a temporary module file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("def greet(name):\n    return f'Hello, {name}'\n")
            tmp_path = Path(f.name)

        try:
            func = import_from_path(str(tmp_path), "greet")
            assert func("World") == "Hello, World"
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_import_class(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("class Person:\n    def __init__(self, name):\n        self.name = name\n")
            tmp_path = Path(f.name)

        try:
            Person = import_from_path(str(tmp_path), "Person")
            p = Person("Alice")
            assert p.name == "Alice"
        finally:
            tmp_path.unlink(missing_ok=True)


class TestValidatePackageStructure:
    def test_valid_package(self, tmp_path):
        pkg = tmp_path / "mypkg"
        pkg.mkdir()
        (pkg / "__init__.py").touch()
        (pkg / "module.py").touch()
        issues = validate_package_structure(str(pkg))
        assert issues == []

    def test_missing_init(self, tmp_path):
        pkg = tmp_path / "badpkg"
        pkg.mkdir()
        issues = validate_package_structure(str(pkg))
        assert any("__init__.py" in issue for issue in issues)

    def test_not_a_directory(self, tmp_path):
        f = tmp_path / "notadir"
        f.write_text("content")
        issues = validate_package_structure(str(f))
        assert any("directory" in issue.lower() for issue in issues)


class TestDetectCircularImports:
    def test_no_cycle(self):
        deps = {"a": ["b"], "b": ["c"], "c": []}
        assert detect_circular_imports(deps) == []

    def test_simple_cycle(self):
        deps = {"a": ["b"], "b": ["a"]}
        cycles = detect_circular_imports(deps)
        assert len(cycles) > 0

    def test_three_way_cycle(self):
        deps = {"a": ["b"], "b": ["c"], "c": ["a"]}
        cycles = detect_circular_imports(deps)
        assert len(cycles) > 0


class TestCreateInitReexport:
    def test_basic(self):
        exports = ["ClassA", "ClassB", "function_c"]
        result = create_init_reexport(exports)
        for name in exports:
            assert name in result


class TestFilterImports:
    def test_basic(self):
        result = filter_imports(
            ["os", "math", "numpy", "requests"],
            allowed=["os", "math", "sys", "json"],
        )
        assert result == ["os", "math"]

    def test_disallowed_imports(self):
        disallowed = filter_imports(
            ["secret_module", "os"],
            allowed=["os"],
        )
        assert "secret_module" not in disallowed
        assert "os" in disallowed
```

- [ ] **Step 2: Write complete/practice.py**

```python
"""Module 05: Modules and Packages — Reference Implementation."""

import importlib.util
import sys
from pathlib import Path
from collections import defaultdict


def import_from_path(module_path, symbol_name):
    """Dynamically import a symbol from a module at a given file path.

    Uses importlib — the programmatic import API. This is what Python itself
    uses internally when you write 'import foo'.
    """
    path = Path(module_path).resolve()
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return getattr(module, symbol_name)


def validate_package_structure(package_dir):
    """Validate a directory is a proper Python package. Return list of issues."""
    issues = []
    path = Path(package_dir)
    if not path.is_dir():
        issues.append(f"'{package_dir}' is not a directory")
        return issues
    if not (path / "__init__.py").exists():
        issues.append(f"Missing __init__.py in '{package_dir}'")
    return issues


def detect_circular_imports(dependencies):
    """Detect circular imports. dependencies is a dict of module_name -> list[dep_name].

    Returns list of cycles found. Uses DFS with tracking of the current path.
    """
    cycles = []
    visited = set()
    path = []

    def dfs(node):
        if node in path:
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        path.append(node)
        for neighbor in dependencies.get(node, []):
            dfs(neighbor)
        path.pop()

    for node in dependencies:
        dfs(node)
    return cycles


def create_init_reexport(exports):
    """Generate __init__.py content that re-exports the given names."""
    lines = [f"from .module import {', '.join(exports)}", ""]
    lines.append(f"__all__ = {exports!r}")
    return "\n".join(lines) + "\n"


def filter_imports(imports, allowed):
    """Filter a list of module names to only those in the allowed set."""
    return [m for m in imports if m in set(allowed)]
```

- [ ] **Step 3: Write initial/practice.py**

```python
"""Module 05: Modules and Packages — Your Implementation."""


def import_from_path(module_path, symbol_name):
    """Dynamically import a symbol from a module at a given file path.

    Use importlib.util.spec_from_file_location + importlib.util.module_from_spec.
    Java analogy: URLClassLoader loading a class from a JAR at runtime.

    Steps:
    1. Create a module spec from the file path
    2. Create a module from the spec
    3. Execute the module (this runs its code)
    4. Return the requested symbol with getattr()
    """
    raise NotImplementedError("TODO: implement import_from_path")


def validate_package_structure(package_dir):
    """Validate a directory is a proper Python package. Return list of issues.

    A valid package must:
    - Be a directory (not a file)
    - Contain __init__.py
    """
    raise NotImplementedError("TODO: implement validate_package_structure")


def detect_circular_imports(dependencies):
    """Detect circular imports using DFS.

    dependencies: dict of module_name -> list of module_names it imports.
    Return list of cycles found. Each cycle is a list of module names.

    Java analogy: detecting circular dependencies in Maven/Bazel build graph.
    """
    raise NotImplementedError("TODO: implement detect_circular_imports")


def create_init_reexport(exports):
    """Generate __init__.py content that re-exports the given names.

    Should produce something like:
        from .module import ClassA, ClassB
        __all__ = ['ClassA', 'ClassB']
    """
    raise NotImplementedError("TODO: implement create_init_reexport")


def filter_imports(imports, allowed):
    """Filter a list of module names to only those in the allowed set.

    Java analogy: classpath filtering or module allowlist in Maven.
    """
    raise NotImplementedError("TODO: implement filter_imports")
```

- [ ] **Step 4: Create run_test.py** — copy from Module 01

- [ ] **Step 5: Create tutorial.ipynb**

```bash
python -c "
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}

nb.cells = [
    nbf.v4.new_markdown_cell('''# Module 05: Modules and Packages for Java Developers

## Java Recall

```java
// File must be at: src/main/java/com/example/bank/Account.java
package com.example.bank;  // Must match directory structure

import com.example.util.Logger;  // Explicit import

public class Account { }
```

- Package declaration MUST match directory path
- One public class per file
- Maven/Gradle manage dependencies and classpath
- Classpath is a JVM argument (-cp or CLASSPATH env var)'''),

    nbf.v4.new_markdown_cell('''## Python Way

```python
# File at: bank/accounts.py — NO package declaration needed!
# Directory structure IS the package structure

# Absolute import
from bank.utils import format_currency

# Relative import (within package)
from .utils import format_currency
from ..common import validators  # parent package

# Dynamic import
import importlib
module = importlib.import_module(\"bank.accounts\")
```

**No package declaration, no one-class-per-file, no build tool required.** The filesystem IS the module namespace.'''),

    nbf.v4.new_markdown_cell('''## Key Differences

| Concept | Java | Python |
|---------|------|--------|
| Package declaration | `package com.foo;` — must match path | No declaration — directory IS package |
| Import | `import com.foo.Bar;` — explicit | `import foo.bar` — dynamic, import hooks exist |
| Classpath | `-cp` or `CLASSPATH` | `sys.path` (list of directories) |
| Build tool | Maven / Gradle | pip / uv / poetry |
| Dependency lock | `pom.xml` / `build.gradle` | `requirements.txt` / `pyproject.toml` / lock file |
| One class per file | Convention (public classes) | No restriction — any number per file |
| __init__.py | No equivalent | Marks directory as package, can run init code |
| Namespace packages | No | Implicit namespace packages (PEP 420, Python 3.3+) |
| Circular imports | Compile error | Runtime ImportError — harder to catch |'''),

    nbf.v4.new_markdown_cell('''## Pitfalls and Interview Traps

### 1. `import` is an executable statement, not a compile-time directive
```python
if some_condition:
    import numpy  # Only imported if condition is True
else:
    import pandas  # Alternative
```
This is perfectly valid. Imports can be conditional, lazy, or even wrapped in try/except.

### 2. Circular imports
```python
# a.py
from b import func_b  # b.py hasn't finished executing yet!
def func_a(): pass

# b.py
from a import func_a  # a.py hasn't finished executing yet!
def func_b(): pass

# ImportError or AttributeError at runtime
```
**Fix:** Move the import inside the function (lazy import), or restructure to break the cycle.

### 3. `__init__.py` executes on import
```python
# mypackage/__init__.py
print(\"Initializing mypackage\")  # Runs when you do 'import mypackage'
```
Use for: re-exporting symbols, running initialization, defining `__all__`.

### 4. `sys.path` controls import resolution
```python
import sys
print(sys.path)  # [current dir, PYTHONPATH entries, stdlib, site-packages]
```
This is Python's classpath. Modify it at runtime to control where imports come from.

### 5. Virtual environments = isolated classpaths
```bash
uv venv                    # Create isolated environment
source .venv/bin/activate  # Activate (modifies PATH and sys.path)
```
Each venv has its own `site-packages/` — like each Maven project having its own `.m2/repository`.'''),

    nbf.v4.new_markdown_cell('''## Your Practice

Open `initial/practice.py`. Implement:

1. **import_from_path** — Dynamic import (importlib)
2. **validate_package_structure** — Check __init__.py
3. **detect_circular_imports** — Graph cycle detection
4. **create_init_reexport** — Generate __init__.py
5. **filter_imports** — Allowlist filtering

Run: `python run_test.py initial` / `python run_test.py complete`.'''),

    nbf.v4.new_markdown_cell('''## References

- [Python Import System](https://docs.python.org/3/reference/import.html)
- [importlib Documentation](https://docs.python.org/3/library/importlib.html)
- [PEP 420 — Implicit Namespace Packages](https://peps.python.org/pep-0420/)
'''),
]

nbf.write(nb, 'modules/05-modules-and-packages/tutorial.ipynb')
"
```

- [ ] **Step 6: Verify and commit**

```bash
cd modules/05-modules-and-packages && python run_test.py complete && git add modules/05-modules-and-packages/ && git commit -m "feat(05): add modules and packages module"
```

---

### Task 10: Module 06 — Decorators and Context Managers

**Files:**
- Create: `modules/06-decorators-and-context-managers/test_practice.py`
- Create: `modules/06-decorators-and-context-managers/complete/practice.py`
- Create: `modules/06-decorators-and-context-managers/initial/practice.py`
- Create: `modules/06-decorators-and-context-managers/run_test.py`
- Create: `modules/06-decorators-and-context-managers/tutorial.ipynb`

- [ ] **Step 1: Write test_practice.py**

```python
"""Tests for Module 06: Decorators and Context Managers."""
import os
import sys
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

import pytest
from practice import timer, retry, memoize, TimedOpen, validate_types


class TestTimer:
    def test_returns_result(self):
        @timer
        def slow_add(a, b):
            time.sleep(0.01)
            return a + b

        result = slow_add(1, 2)
        assert result == 3

    def test_preserves_metadata(self):
        @timer
        def documented_func():
            """Docstring here."""
            pass

        assert documented_func.__name__ == "documented_func"
        assert documented_func.__doc__ == "Docstring here."


class TestRetry:
    def test_succeeds_first_try(self):
        call_count = 0

        @retry(max_attempts=3, exceptions=(ValueError,))
        def maybe_fail():
            nonlocal call_count
            call_count += 1
            return "ok"

        result = maybe_fail()
        assert result == "ok"
        assert call_count == 1

    def test_retries_on_exception(self):
        call_count = 0

        @retry(max_attempts=3, exceptions=(ValueError,))
        def fails_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("transient error")
            return "recovered"

        result = fails_twice()
        assert result == "recovered"
        assert call_count == 3

    def test_exhausts_retries(self):
        @retry(max_attempts=2, exceptions=(ValueError,))
        def always_fails():
            raise ValueError("persistent error")

        with pytest.raises(ValueError, match="persistent error"):
            always_fails()


class TestMemoize:
    def test_caches_results(self):
        call_count = 0

        @memoize
        def expensive(n):
            nonlocal call_count
            call_count += 1
            return n * 2

        assert expensive(5) == 10
        assert expensive(5) == 10  # cached
        assert call_count == 1     # only called once

    def test_different_args(self):
        @memoize
        def add(a, b):
            return a + b

        assert add(1, 2) == 3
        assert add(2, 3) == 5


class TestTimedOpen:
    def test_writes_and_reads(self, tmp_path):
        filepath = tmp_path / "test.txt"
        with TimedOpen(filepath, "w") as f:
            f.write("hello")

        assert filepath.read_text() == "hello"

    def test_file_closed_after_with(self, tmp_path):
        filepath = tmp_path / "test.txt"
        with TimedOpen(filepath, "w") as f:
            f.write("data")

        assert f.closed is True


class TestValidateTypes:
    def test_valid_types(self):
        @validate_types
        def greet(name: str, times: int) -> str:
            return name * times

        assert greet("hi", 3) == "hihihi"

    def test_invalid_type_raises(self):
        @validate_types
        def greet(name: str, times: int) -> str:
            return name * times

        with pytest.raises(TypeError):
            greet("hi", "not_an_int")

    def test_no_annotations_passes(self):
        @validate_types
        def no_hints(a, b):
            return a + b

        assert no_hints(1, 2) == 3
```

- [ ] **Step 2: Write complete/practice.py**

```python
"""Module 06: Decorators and Context Managers — Reference Implementation."""

import functools
import inspect
import time
from pathlib import Path


def timer(func):
    """Decorator that prints the execution time of the decorated function.

    Java analogy: AOP (Aspect-Oriented Programming) — wrapping a method
    with cross-cutting behavior. But Java annotations are metadata, while
    Python decorators are runtime transformations.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timer] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def retry(max_attempts=3, exceptions=(Exception,)):
    """Parameterized decorator: retry the function on specified exceptions.

    Demonstrates the decorator factory pattern — a function that returns
    a decorator. This is how you create decorators that accept arguments.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == max_attempts:
                        raise
            return None  # unreachable
        return wrapper
    return decorator


def memoize(func):
    """Simple memoization decorator — caches function return values by arguments.

    Like @Cacheable in Spring, but implemented in 5 lines.
    python 3.9+ has functools.cache as a built-in.
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper


class TimedOpen:
    """Context manager wrapping open() that logs how long the file was open.

    Demonstrates the context manager protocol: __enter__ + __exit__.
    Java analogy: try-with-resources (AutoCloseable).
    """
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
        return False  # Don't suppress exceptions


def validate_types(func):
    """Decorator that checks argument types match annotations at runtime.

    Python type hints are normally ignored at runtime — this decorator
    enforces them. Not for production use, but demonstrates that annotations
    ARE accessible at runtime via func.__annotations__.
    """
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
                        f"Argument '{name}' expected {expected.__name__}, got {type(value).__name__}"
                    )

        return func(*args, **kwargs)

    return wrapper
```

- [ ] **Step 3: Write initial/practice.py**

```python
"""Module 06: Decorators and Context Managers — Your Implementation."""


def timer(func):
    """Decorator that prints execution time of the decorated function.

    @timer
    def my_func():
        ...

    A decorator is a function that takes a function and returns a new function.
    Use functools.wraps(func) to preserve metadata (__name__, __doc__).
    Use time.perf_counter() for high-resolution timing.

    Java analogy: @Timer is like a Spring AOP @Around advice.
    CRITICAL DIFFERENCE: Java annotations are passive metadata.
    Python decorators are active — they REPLACE the function at definition time.
    """
    raise NotImplementedError("TODO: implement timer decorator")


def retry(max_attempts=3, exceptions=(Exception,)):
    """Parameterized decorator: retry on specified exceptions up to max_attempts.

    @retry(max_attempts=3, exceptions=(ValueError, ConnectionError))
    def flaky_operation():
        ...

    This is a decorator FACTORY — it returns a decorator, which returns a wrapper.
    Three levels of functions. Take a deep breath.
    """
    raise NotImplementedError("TODO: implement retry decorator")


def memoize(func):
    """Memoization decorator — cache results by arguments.

    @memoize
    def fib(n): ...

    Use a dict for the cache. functools.cache does this in stdlib as of Python 3.9.
    """
    raise NotImplementedError("TODO: implement memoize decorator")


class TimedOpen:
    """Context manager wrapping open() that logs how long the file was open.

    with TimedOpen('file.txt', 'w') as f:
        f.write('data')

    Context manager protocol:
    - __enter__(self) — called on entry, return value assigned to 'as f'
    - __exit__(self, exc_type, exc_val, exc_tb) — called on exit (even on exception)

    Java analogy: try-with-resources (AutoCloseable interface).
    """
    raise NotImplementedError("TODO: implement TimedOpen context manager")


def validate_types(func):
    """Decorator that checks argument types match annotations at runtime.

    @validate_types
    def greet(name: str, times: int) -> str:
        return name * times

    Access annotations via func.__annotations__ — it's a dict.
    Use inspect.signature(func) to bind arguments to parameter names.
    """
    raise NotImplementedError("TODO: implement validate_types decorator")
```

- [ ] **Step 4: Create run_test.py** — copy from Module 01

- [ ] **Step 5: Create tutorial.ipynb**

```bash
python -c "
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}

nb.cells = [
    nbf.v4.new_markdown_cell('''# Module 06: Decorators and Context Managers

## Interview Pro-Tip

\"Are Python decorators like Java annotations?\" — This is a TRAP question.
The answer is NO, they are fundamentally different. Understanding WHY is
what separates candidates who get it from those who don't.'''),

    nbf.v4.new_markdown_cell('''## Java Recall

```java
// Annotations are passive metadata
@Timed  // This attaches metadata to the method
@Retry(maxAttempts = 3)
public String fetchData() {
    // Some framework reads the annotation and applies behavior
    // The annotation itself does NOTHING at runtime
}

// try-with-resources for resource management
try (FileWriter f = new FileWriter(\"output.txt\")) {
    f.write(\"data\");
} // Auto-close guaranteed
```

Java annotations are **metadata** — they don't change the code. A framework
(Spring, JUnit, AspectJ) reads them and acts on them. The annotation exists
without the framework — it's just inert information.'''),

    nbf.v4.new_markdown_cell('''## Python Way

```python
# Decorators are ACTIVE transformations at definition time
@timer  # This REPLACES the function with a wrapped version
def slow_function():
    time.sleep(1)
    return \"done\"

# @timer is syntactic sugar for:
# slow_function = timer(slow_function)

# Context manager protocol
with open(\"file.txt\", \"w\") as f:  # __enter__ called
    f.write(\"data\")
# __exit__ called automatically — even if an exception occurs
```

**Critical difference:** `@timer` transforms the function **at definition time**.
The original function is gone — replaced by the wrapped version. No framework needed.
This is a language feature, not a configuration system.'''),

    nbf.v4.new_markdown_cell('''## Key Differences

| Concept | Java | Python |
|---------|------|--------|
| Annotation / Decorator | Metadata — inert without framework | Function transformation at definition time |
| Activation | Framework/container processes it | Language runtime applies it |
| Without framework | Annotation exists, does nothing | Decorator still works — no framework needed |
| Arguments | `@Retry(max=3)` — attribute syntax | `@retry(max_attempts=3)` — function call that returns a decorator |
| Resource management | try-with-resources (AutoCloseable) | `with` statement (context manager protocol) |
| Protocol for `with` | `AutoCloseable.close()` | `__enter__()` + `__exit__()` |'''),

    nbf.v4.new_markdown_cell('''## Deep Dive: How Decorators Work

```python
# A decorator is just a function that takes a function and returns a function
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(\"Before\")
        result = func(*args, **kwargs)
        print(\"After\")
        return result
    return wrapper

# These are equivalent:
@my_decorator
def say_hello(): ...

def say_hello(): ...
say_hello = my_decorator(say_hello)  # Same thing!
```

**Parameterized decorators** add one more level:
```python
def retry(max_attempts):        # Level 1: takes config
    def decorator(func):         # Level 2: takes the function (this is the decorator)
        def wrapper(*args):      # Level 3: replaces the function
            for _ in range(max_attempts):
                try: return func(*args)
                except: pass
            raise
        return wrapper
    return decorator

@retry(max_attempts=3)  # retry(3) returns the decorator, which is applied to func
def flaky(): ...
```'''),

    nbf.v4.new_markdown_cell('''## Your Practice

Open `initial/practice.py`. Implement:

1. **@timer** — Simple decorator (4-6 lines)
2. **@retry(max_attempts, exceptions)** — Parameterized decorator (10-12 lines)
3. **@memoize** — Caching decorator (8-10 lines)
4. **TimedOpen** — Context manager class (15-20 lines)
5. **@validate_types** — Runtime type checking decorator (15-18 lines)

Run: `python run_test.py initial` / `python run_test.py complete`.'''),

    nbf.v4.new_markdown_cell('''## References

- [PEP 318 — Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
- [PEP 343 — The \"with\" Statement](https://peps.python.org/pep-0343/)
- [functools.wraps](https://docs.python.org/3/library/functools.html#functools.wraps)
'''),
]

nbf.write(nb, 'modules/06-decorators-and-context-managers/tutorial.ipynb')
"
```

- [ ] **Step 6: Verify and commit**

```bash
cd modules/06-decorators-and-context-managers && python run_test.py complete && git add modules/06-decorators-and-context-managers/ && git commit -m "feat(06): add decorators and context managers module"
```

---

### Task 11: Module 07 — Type Hints

**Files:**
- Create: `modules/07-type-hints/test_practice.py`
- Create: `modules/07-type-hints/complete/practice.py`
- Create: `modules/07-type-hints/initial/practice.py`
- Create: `modules/07-type-hints/run_test.py`
- Create: `modules/07-type-hints/tutorial.ipynb`

- [ ] **Step 1: Write test_practice.py**

```python
"""Tests for Module 07: Type Hints."""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

import pytest
from practice import Stack, first, typed_deserialize


class TestStack:
    def test_push_pop_int(self):
        s = Stack[int]()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        assert s.pop() == 1

    def test_push_pop_str(self):
        s = Stack[str]()
        s.push("a")
        s.push("b")
        assert s.pop() == "b"

    def test_empty_raises(self):
        s = Stack[int]()
        with pytest.raises(IndexError, match="empty"):
            s.pop()

    def test_len(self):
        s = Stack[int]()
        s.push(1)
        s.push(2)
        assert len(s) == 2

    def test_bool(self):
        s = Stack[int]()
        assert bool(s) is False
        s.push(1)
        assert bool(s) is True


class TestFirst:
    def test_non_empty_list(self):
        result = first([1, 2, 3])
        assert result == 1

    def test_empty_returns_none(self):
        assert first([]) is None

    def test_strings(self):
        assert first(["hello", "world"]) == "hello"


class TestTypedDeserialize:
    def test_basic_dict(self):
        data = {"name": "Alice", "age": 30}
        result = typed_deserialize(data, dict)
        assert result["name"] == "Alice"
        assert result["age"] == 30

    def test_int_coercion(self):
        result = typed_deserialize(42, str)
        assert result == "42"

    def test_list_element_coercion(self):
        result = typed_deserialize(["1", "2", "3"], list[int])
        assert result == [1, 2, 3]
```

- [ ] **Step 2: Write complete/practice.py**

```python
"""Module 07: Type Hints — Reference Implementation."""

from typing import Generic, TypeVar, Sequence, get_origin, get_args

T = TypeVar("T")


class Stack(Generic[T]):
    """A generic stack. Stack[int] creates a stack of integers.

    Java analogy: Stack<Integer> — same syntax, similar concept.
    Key difference: Python generics are ERASED at runtime (like Java).
    The type parameter is only for static checkers (mypy).
    """
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
    """Return the first element of a sequence, or None if empty.

    Sequence[T] accepts list[T], tuple[T], str, bytes, etc.
    T | None (Python 3.10+) is equivalent to Optional[T].
    """
    return items[0] if items else None


def typed_deserialize(data, target_type):
    """Coerce data to the target type if possible.

    Demonstrates runtime type introspection using typing.get_origin() and
    typing.get_args(). This is how you inspect generic types at runtime
    (e.g., list[int] -> origin=list, args=(int,)).

    Java analogy: Jackson's TypeReference<T> for deserializing generics.
    """
    origin = get_origin(target_type)

    if origin is list:
        (item_type,) = get_args(target_type)
        return [typed_deserialize(item, item_type) for item in data]

    if target_type is str and not isinstance(data, str):
        return str(data)

    if target_type is int and isinstance(data, str):
        return int(data)

    return data
```

- [ ] **Step 3: Write initial/practice.py**

```python
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
```

- [ ] **Step 4: Create run_test.py** — copy from Module 01

- [ ] **Step 5: Create tutorial.ipynb**

```bash
python -c "
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}

nb.cells = [
    nbf.v4.new_markdown_cell('''# Module 07: Type Hints for Java Developers

## Java Recall

```java
// Java: types are mandatory, checked at compile time
public class Stack<T> {
    private List<T> items = new ArrayList<>();

    public void push(T item) { items.add(item); }
    public T pop() { return items.remove(items.size() - 1); }
}

Stack<Integer> intStack = new Stack<>();
intStack.push(42);
intStack.push(\"hello\");  // COMPILE ERROR — caught immediately
```

Java's type system is NOMINAL and checked at compile time. If it compiles, the types are correct. Generics are erased at runtime (type erasure), same as Python.'''),

    nbf.v4.new_markdown_cell('''## Python Way

```python
from typing import Generic, TypeVar

T = TypeVar(\"T\")  # Like Java's <T>

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Usage — types are OPTIONAL
stack: Stack[int] = Stack()  # Type checker enforces this
stack.push(42)
stack.push(\"hello\")  # mypy ERROR, but Python runs it anyway!
```

**The big difference:** Python type hints are NEVER enforced at runtime. They are documentation that a static checker (mypy, pyright) verifies. The interpreter ignores them completely. This is called GRADUAL TYPING — you add types where they help, skip them where they don't.'''),

    nbf.v4.new_markdown_cell('''## Key Differences

| Concept | Java | Python |
|---------|------|--------|
| Type checking | Compile-time, mandatory | Optional, via mypy/pyright |
| Runtime enforcement | JVM verifies bytecode | None — hints are ignored |
| Generics | `<T>` — type erasure | `Generic[T]` — also type erasure |
| Null safety | `@Nullable` / `Optional<T>` / Kotlin-style | `T | None` (3.10+) / `Optional[T]` |
| Type alias | Not directly | `type Point = tuple[float, float]` (3.12+) |
| Data class | `record` (Java 14+) | `dataclass` decorator |
| Sealed types | `sealed` (Java 17+) | `Literal`, `Union`, type narrowing |
| Structural typing | No (nominal only) | Protocol (like Go interfaces) |
| Type variable bounds | `<T extends Comparable<T>>` | `T = TypeVar('T', bound=Comparable)` |'''),

    nbf.v4.new_markdown_cell('''## Pitfalls and Interview Traps

### 1. Type hints don't make Python type-safe at runtime
```python
def add(a: int, b: int) -> int:
    return a + b

add(\"hello\", \"world\")  # Runs fine! Returns \"helloworld\"
```
Mypy catches this, but Python doesn't. Unlike Java, type errors that aren't
caught by mypy become runtime bugs.

### 2. `list[int]` vs `List[int]` (Python 3.9+)
```python
# Python 3.9+ (preferred):
def process(items: list[int]) -> dict[str, int]: ...

# Python 3.8 and earlier (deprecated in 3.9+):
from typing import List, Dict
def process(items: List[int]) -> Dict[str, int]: ...
```
Use the lowercase built-in generics in modern code (3.12+).

### 3. Generics are erased, but you can introspect them
```python
from typing import get_origin, get_args

t = list[int]
print(get_origin(t))   # <class 'list'>
print(get_args(t))     # (<class 'int'>,)
```
Unlike Java, Python makes generic type arguments accessible at runtime via the typing module. This is useful for serialization/deserialization frameworks.

### 4. Covariance and contravariance
```python
T_co = TypeVar('T_co', covariant=True)   # Read-only containers
T_contra = TypeVar('T_contra', contravariant=True)  # Write-only consumers
```
Like Java's `<? extends T>` (covariant) and `<? super T>` (contravariant).'''),

    nbf.v4.new_markdown_cell('''## Your Practice

Open `initial/practice.py`. Implement:

1. **Stack[T]** — Generic class with TypeVar
2. **first** — Type-safe first-element function
3. **typed_deserialize** — Runtime generic type coercion (uses get_origin/get_args)

Run: `python run_test.py initial` / `python run_test.py complete`.'''),

    nbf.v4.new_markdown_cell('''## References

- [typing — Support for type hints](https://docs.python.org/3/library/typing.html)
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/)
- [mypy documentation](https://mypy.readthedocs.io/)
'''),
]

nbf.write(nb, 'modules/07-type-hints/tutorial.ipynb')
"
```

- [ ] **Step 6: Verify and commit**

```bash
cd modules/07-type-hints && python run_test.py complete && git add modules/07-type-hints/ && git commit -m "feat(07): add type hints module"
```

---

### Task 12: Module 08 — Concurrency and Parallelism

**Files:**
- Create: `modules/08-concurrency-and-parallelism/test_practice.py`
- Create: `modules/08-concurrency-and-parallelism/complete/practice.py`
- Create: `modules/08-concurrency-and-parallelism/initial/practice.py`
- Create: `modules/08-concurrency-and-parallelism/run_test.py`
- Create: `modules/08-concurrency-and-parallelism/tutorial.ipynb`

- [ ] **Step 1: Write test_practice.py**

```python
"""Tests for Module 08: Concurrency and Parallelism."""
import os
import sys
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

import pytest
from practice import (
    sequential_sum,
    threaded_sum,
    process_sum,
    gil_demonstration,
    countdown,
)


def is_prime(n):
    """Simple deterministic primality test for benchmarking."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


class TestSequentialSum:
    def test_sum_range(self):
        assert sequential_sum(range(1, 101)) == 5050

    def test_empty(self):
        assert sequential_sum([]) == 0


class TestThreadedSum:
    def test_sum_range_2_threads(self):
        result = threaded_sum(range(1, 101), num_threads=2)
        assert result == 5050

    def test_sum_range_4_threads(self):
        result = threaded_sum(range(1, 101), num_threads=4)
        assert result == 5050


class TestProcessSum:
    def test_sum_range(self):
        result = process_sum(range(1, 101), num_processes=2)
        assert result == 5050


class TestGILDemonstration:
    def test_returns_dict_with_expected_keys(self):
        result = gil_demonstration()
        assert "sequential_time" in result
        assert "threaded_time" in result
        assert isinstance(result["sequential_time"], float)
        assert isinstance(result["threaded_time"], float)


class TestCountdown:
    def test_returns_list(self):
        result = countdown(3)
        assert result == [3, 2, 1, "go!"]
```

- [ ] **Step 2: Write complete/practice.py**

```python
"""Module 08: Concurrency and Parallelism — Reference Implementation."""

import concurrent.futures
import math
import multiprocessing
import threading
import time


def sequential_sum(iterable):
    """Sum an iterable in a single thread. Baseline for comparison."""
    return sum(iterable)


def _chunked_sum(args):
    """Worker: sum a slice of the data."""
    data_slice, start, end = args
    return sum(data_slice[start:end])


def _make_chunks(data, num_chunks):
    """Split data into roughly equal chunks."""
    n = len(data)
    chunk_size = math.ceil(n / num_chunks)
    chunks = []
    for i in range(0, n, chunk_size):
        chunks.append((data, i, min(i + chunk_size, n)))
    return chunks


def threaded_sum(iterable, num_threads=4):
    """Sum using threading — good for I/O, NOT faster for CPU (due to GIL).

    This demonstrates WHY threading doesn't help CPU-bound work in Python.
    For I/O-bound work (network, disk), threading works fine because the GIL
    is released during I/O operations.
    """
    data = list(iterable)
    chunks = _make_chunks(data, num_threads)
    total = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for result in executor.map(_chunked_sum, chunks):
            total += result
    return total


def process_sum(iterable, num_processes=4):
    """Sum using multiprocessing — actually parallel for CPU-bound work.

    Each process has its OWN Python interpreter and its OWN GIL.
    This is the standard library way to parallelize CPU-bound tasks.
    """
    data = list(iterable)
    chunks = _make_chunks(data, num_processes)
    total = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        for result in executor.map(_chunked_sum, chunks):
            total += result
    return total


def _cpu_heavy_work():
    """Simulate CPU-bound computation."""
    total = 0
    for i in range(5_000_000):
        total += i
    return total


def gil_demonstration():
    """Demonstrate GIL impact: compare sequential vs threaded for CPU work.

    Returns a dict with timing info. On most systems, threaded_time >= sequential_time
    because the GIL prevents true parallel execution of Python bytecode.
    """
    # Sequential
    start = time.perf_counter()
    for _ in range(4):
        _cpu_heavy_work()
    sequential_time = time.perf_counter() - start

    # Threaded
    start = time.perf_counter()
    threads = []
    for _ in range(4):
        t = threading.Thread(target=_cpu_heavy_work)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    threaded_time = time.perf_counter() - start

    return {
        "sequential_time": sequential_time,
        "threaded_time": threaded_time,
    }


def countdown(n):
    """Simple function to verify module works. Not concurrency-related."""
    return list(range(n, 0, -1)) + ["go!"]
```

- [ ] **Step 3: Write initial/practice.py**

```python
"""Module 08: Concurrency and Parallelism — Your Implementation."""


def sequential_sum(iterable):
    """Sum an iterable in a single thread. This is the baseline.

    Just use the built-in sum() function.
    """
    raise NotImplementedError("TODO: implement sequential_sum")


def threaded_sum(iterable, num_threads=4):
    """Sum using threading.Thread or ThreadPoolExecutor.

    KEY INSIGHT: Due to the GIL, this will NOT be faster than sequential_sum
    for CPU-bound work. Only one thread executes Python bytecode at a time.

    For I/O-bound work (reading files, network requests), threads ARE useful
    because the GIL is released during I/O operations.

    Use concurrent.futures.ThreadPoolExecutor.
    """
    raise NotImplementedError("TODO: implement threaded_sum")


def process_sum(iterable, num_processes=4):
    """Sum using multiprocessing. Each process has its own Python interpreter + GIL.

    This IS truly parallel for CPU-bound work. The cost: spawning processes is
    expensive (pickle serialization, memory copy on some platforms).

    Use concurrent.futures.ProcessPoolExecutor.
    """
    raise NotImplementedError("TODO: implement process_sum")


def _cpu_heavy_work():
    """Simulate CPU-bound computation."""
    total = 0
    for i in range(5_000_000):
        total += i
    return total


def gil_demonstration():
    """Demonstrate GIL impact: compare sequential vs threaded for CPU work.

    Run _cpu_heavy_work() 4 times:
    1. Sequentially (one after another)
    2. In 4 threads (supposedly concurrent)

    Return a dict with 'sequential_time' and 'threaded_time'.
    In most cases, threaded_time will be >= sequential_time.
    """
    raise NotImplementedError("TODO: implement gil_demonstration")


def countdown(n):
    """Simple function to verify module works. Return list from n down to 1, then 'go!'."""
    raise NotImplementedError("TODO: implement countdown")
```

- [ ] **Step 4: Create run_test.py** — copy from Module 01

- [ ] **Step 5: Create tutorial.ipynb**

```bash
python -c "
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}}

nb.cells = [
    nbf.v4.new_markdown_cell('''# Module 08: Concurrency and Parallelism for Java Developers

## Interview Pro-Tip

This module covers THE most common Python interview question for backend engineers:
**\"What is the GIL and how do you run CPU-bound tasks in parallel?\"**'''),

    nbf.v4.new_markdown_cell('''## Java Recall

```java
// Java threads ARE parallel (for CPU work)
ExecutorService executor = Executors.newFixedThreadPool(4);
List<Future<Integer>> futures = new ArrayList<>();

for (int i = 0; i < 4; i++) {
    futures.add(executor.submit(() -> heavyComputation()));
}

for (Future<Integer> f : futures) {
    total += f.get();  // Wait for each to complete
}
executor.shutdown();
```

In Java, threads give you real parallelism on multi-core CPUs. The JVM has no GIL.
For CPU-bound work, you use threads. For I/O-bound, you use async/CompletableFuture or threads.'''),

    nbf.v4.new_markdown_cell('''## Python Way — The GIL

### What is the GIL?

The **Global Interpreter Lock** (GIL) is a mutex that prevents multiple threads from
executing Python bytecode simultaneously. Only ONE thread can hold the GIL at any moment.

### Why does it exist?

CPython's memory management uses reference counting (not a tracing GC like Java).
Every object has a refcount that gets incremented/decremented. Without a lock, two
threads modifying the same object's refcount would corrupt memory. The GIL is the
simplest way to make CPython thread-safe internally.

### What this means in practice:

```python
# Threading for CPU work — DOES NOT HELP (GIL!)
import threading

def cpu_heavy():
    for i in range(10**7):
        _ = i * i

# Sequential: 4 tasks take ~4 seconds
# Threaded: 4 tasks still take ~4 seconds (maybe SLOWER due to GIL contention)

# Threading for I/O work — WORKS FINE (GIL released during I/O)
def io_bound():
    time.sleep(1)  # GIL is released during sleep
    requests.get(\"https://api.example.com\")  # GIL released during network I/O

# Sequential: 4 tasks take ~4 seconds
# Threaded: 4 tasks take ~1 second (actual concurrency!)
```

The GIL is released during I/O operations, C extension calls, and `time.sleep()`.'''),

    nbf.v4.new_markdown_cell('''## Three Ways to Achieve Parallelism (Without Third-Party Libraries)

### 1. `multiprocessing` — Separate processes, separate GILs
```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(cpu_heavy, data)  # Truly parallel!
```
Each process has its own Python interpreter and its own GIL. The cost: pickling data
between processes, memory overhead per process, slower startup.

### 2. `concurrent.futures` — Unified API for threads and processes
```python
# I/O-bound: ThreadPoolExecutor
with ThreadPoolExecutor() as pool:
    results = pool.map(fetch_url, urls)

# CPU-bound: ProcessPoolExecutor
with ProcessPoolExecutor() as pool:
    results = pool.map(compute, data)
```
Same API, different executor. This is the modern (Python 3.2+) recommended approach.

### 3. `asyncio` — Cooperative multitasking (single-threaded)
```python
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)

asyncio.run(main())
```
Single-threaded, cooperative, event-loop based. Great for high-concurrency I/O.
NOT for CPU work. Think of it as Node.js's event loop, but with nicer syntax.'''),

    nbf.v4.new_markdown_cell('''## Key Differences

| Concept | Java | Python |
|---------|------|--------|
| **Threads are parallel?** | Yes (JVM has no GIL) | No (GIL limits to one thread at a time for Python bytecode) |
| **CPU-bound parallelism** | Threads | `multiprocessing` / `ProcessPoolExecutor` |
| **I/O concurrency** | Threads or CompletableFuture | Threads or `asyncio` |
| **Async model** | CompletableFuture / virtual threads | `asyncio` (explicit async/await) |
| **Data sharing** | Shared memory (with synchronization) | Processes: pickle + IPC / Threads: shared objects (but GIL) |
| **Memory overhead** | Low (threads share heap) | High (each process has own interpreter) |
| **stdin/stdout capture** | Built-in | `subprocess.run(capture_output=True)` |
| **GIL future** | N/A | Being removed (PEP 703, Python 3.13 free-threaded build) |

## Interview Answer Template

**Q: \"How do you run parallel CPU tasks in Python without third-party libraries?\"**

A: \"Python has a GIL, so threading won't help for CPU-bound work. Instead, there are three standard-library options:

1. **`multiprocessing`** — spawn separate Python processes. Each has its own GIL, so they truly run in parallel. Use `ProcessPoolExecutor` for a clean API.

2. **`concurrent.futures`** — provides `ThreadPoolExecutor` (for I/O) and `ProcessPoolExecutor` (for CPU) with the same interface.

3. **`asyncio`** — cooperative multitasking for high-concurrency I/O. Not for CPU work.

For simple cases, `ProcessPoolExecutor.map()` is the modern, cleanest approach.
For complex cases with shared state, `multiprocessing.Queue` and `multiprocessing.Manager`.

Also worth mentioning: Python 3.13+ has a free-threaded build (PEP 703) that removes the GIL experimentally.\"'''),

    nbf.v4.new_markdown_cell('''## Your Practice

Open `initial/practice.py`. Implement:

1. **sequential_sum** — Baseline sum (trivial)
2. **threaded_sum** — Using `ThreadPoolExecutor`
3. **process_sum** — Using `ProcessPoolExecutor`
4. **gil_demonstration** — Compare sequential vs threaded timing
5. **countdown** — Simple function for module sanity check

Run: `python run_test.py initial` / `python run_test.py complete`.'''),

    nbf.v4.new_markdown_cell('''## References

- [Global Interpreter Lock (Python Wiki)](https://wiki.python.org/moin/GlobalInterpreterLock)
- [PEP 703 — Making the GIL Optional](https://peps.python.org/pep-0703/)
- [concurrent.futures — Launching parallel tasks](https://docs.python.org/3/library/concurrent.futures.html)
- [multiprocessing — Process-based parallelism](https://docs.python.org/3/library/multiprocessing.html)
- [asyncio — Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)
'''),
]

nbf.write(nb, 'modules/08-concurrency-and-parallelism/tutorial.ipynb')
"
```

- [ ] **Step 6: Verify and commit**

```bash
cd modules/08-concurrency-and-parallelism && python run_test.py complete && git add modules/08-concurrency-and-parallelism/ && git commit -m "feat(08): add concurrency and parallelism module"
```

---

### Task 13: Final Integration and Validation

**Files:**
- Modify: `pyproject.toml` (no changes needed — verify)

- [ ] **Step 1: Run all module tests against complete/**

```bash
PRACTICE_TARGET=complete pytest modules/ -v
```
Expected: All tests in all 8 modules pass (approximately 100+ tests).

- [ ] **Step 2: Verify all initial/ skeletons fail as expected**

```bash
for d in modules/*/; do
    cd "$d" && python run_test.py initial 2>&1 | head -3
done
```
Expected: Each module shows FAILED/errors (NotImplementedError).

- [ ] **Step 3: Verify project structure is complete**

```bash
find modules -type f | sort
```
Expected: Each of the 8 modules has `tutorial.ipynb`, `test_practice.py`, `run_test.py`, `initial/practice.py`, `complete/practice.py`.

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "chore: final integration — all 8 modules complete and verified"
```
