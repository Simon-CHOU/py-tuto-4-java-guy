# Python Tutorial for Java Devs — Design Spec

**Date:** 2026-05-29
**Status:** Approved

## Overview

An interactive Python tutorial for developers with a Java background, designed to build
interview-ready Python knowledge. Organized around the principle: *new knowledge attaches
best to existing knowledge* — each module starts from a familiar Java concept and maps it
to the Python equivalent.

**Target audience:** A Java developer preparing for a Python-related position who needs to
demonstrate Python awareness in video interview rapid-fire Q&A.

**Non-goal:** Cosplaying as a Python expert. The learner does not need deep Pythonista
idioms — they need clear, defensible answers to common interview questions.

## Toolchain

| Tool | Role | Analogy for Java Dev |
|------|------|---------------------|
| `uv` | Python runtime & dependency management | sdkman + maven/gradle (simplified) |
| `pytest` | Test framework | JUnit 5 (but less boilerplate) |
| `jupyter` | Interactive notebook for teaching | Not a Java analogy — interactive REPL docs |

Tutorial code uses **standard library only** (zero third-party dependencies in
`dependencies`). `pytest` and `jupyter` are dev-only tools in `[project.optional-dependencies] dev`.

## Project Structure

```
pyproject.toml              # uv project config, pytest settings
.venv/                      # uv-managed virtualenv
modules/
  ├── 01-basics-and-types/
  │   ├── tutorial.ipynb
  │   ├── initial/practice.py
  │   ├── complete/practice.py
  │   ├── test_practice.py
  │   └── run_test.py
  ├── 02-functional-features/
  │   └── ... (same structure)
  ├── 03-oop/
  ├── 04-interfaces-and-abstraction/
  ├── 05-modules-and-packages/
  ├── 06-decorators-and-context-managers/
  ├── 07-type-hints/
  └── 08-concurrency-and-parallelism/
docs/                       # Existing reference docs (untouched)
```

## Module List

### 01 — Basics and Types
**Java question:** "int is a primitive, but in Python everything's an object — how does
that even work?"
**Covers:** dynamic typing, `type()` vs `instanceof`, basic types (`int`, `str`, `float`,
`bool`, `None`), control flow differences (no `switch` until 3.10), string formatting.

### 02 — Functional Features
**Java question:** "We have Stream API with map/filter/reduce — what's the Python equivalent?"
**Covers:** comprehensions (`list`/`dict`/`set`/`generator`), `lambda` limitations,
`map`/`filter`/`reduce`, iterator protocol, `yield`/generators, `itertools`.

### 03 — Object-Oriented Programming
**Java question:** "No `private`? Multiple inheritance? What about method overloading?"
**Covers:** class syntax, `self`, `__init__` vs constructor, MRO and `super()`,
dunder methods (`__str__`, `__repr__`, `__eq__`), `@property`, name mangling convention.

### 04 — Interfaces and Abstraction (Interview Hotspot)
**Java question:** "If there's no `interface` keyword, how do I express a contract?"
**Covers:** duck typing, `ABC` + `@abstractmethod`, `Protocol` (structural subtyping),
`@abstractclassmethod`, comparison table: Java interface vs ABC vs Protocol vs duck typing.

### 05 — Modules, Packages, and Project Structure
**Java question:** "No `package` declaration matching directory? No maven? How do you
even organize code?"
**Covers:** `import` system and `sys.path`, `__init__.py`, relative vs absolute imports,
virtual environments (`uv venv`), `pyproject.toml`, namespace packages.

### 06 — Decorators and Context Managers
**Java question:** "Are decorators like Java annotations?"
**Covers:** functions as first-class objects, closure refresher, `@decorator` syntax
(short answer: no, they're fundamentally different — annotations are metadata, decorators
are runtime transformations), writing simple decorators, `functools.wraps`,
`with` statement and context manager protocol.

### 07 — Type Hints and Static Checking
**Java question:** "Can Python type annotations give me real type safety?"
**Covers:** gradual typing philosophy, `mypy` basics, `Protocol`, `Generic`, `TypeVar`,
`dataclass`, `TypedDict`, runtime behavior (hints are ignored at runtime),
contrast with Java's compile-time type checking.

### 08 — Concurrency and Parallelism (Interview Hotspot)
**Java question:** "GIL — what is it, why does it exist, and how do I actually run things in parallel?"
**Covers:** GIL history and rationale, `threading` (I/O-bound), `multiprocessing`
(CPU-bound), `concurrent.futures`, `asyncio` basics, `subprocess`. Comparison table:
Java Thread vs Python threading vs multiprocessing vs asyncio.

## Module Internal Structure

### tutorial.ipynb (6 sections)

1. **Java Recall** — A Java code snippet that activates existing knowledge
2. **Python Way** — Same scenario in Python, with runnable cells
3. **Key Differences** — Comparison table: Java X → Python Y, and *why* they differ
4. **Pitfalls & Interview Traps** — Common "looks the same, works differently" gotchas
5. **Practice Guide** — Points to `initial/` directory, hints on where to start
6. **Reference** — Links to official Python docs for deeper reading

Cells in section 2 are runnable (notebook injects `complete/` into `sys.path`).

### initial/practice.py

- 4-8 functions per module covering core concepts
- ~70% "fill in the blank" (`raise NotImplementedError`)
- ~30% "fix the anti-pattern" (working but wrong code — e.g., mutable default arg)
- Function signatures and imports match `complete/practice.py` exactly

### complete/practice.py

- Full reference implementation
- Written in the most Pythonic, clean style appropriate for the concept
- Passes all tests in `test_practice.py`

### test_practice.py

- Shared pytest file (not duplicated in `initial/` and `complete/`)
- Each test is named after the concept it validates: `test_fib_base_case`, `test_mutable_default_behavior`
- Tests cover both happy path and edge cases / traps
- Run via `run_test.py` (not directly — see below)

### run_test.py

Cross-platform test executor (WSL2 / Win11 / PowerShell / cmd — single command):

```bash
cd modules/01-basics-and-types
python run_test.py initial     # Test your skeleton
python run_test.py complete    # Test the reference answer
```

Internally: sets up `sys.path` to point at the chosen target (`initial/` or `complete/`),
then runs pytest on `test_practice.py`. This avoids environment variable issues
across shells.

## Testing Strategy

- `pytest modules/` at project root runs **all** module tests (validates `complete` answers)
- Per-module learning loop: `python run_test.py initial` → fail → write code → pass
- After completing a module: `python run_test.py complete` to compare with reference
- No `initial/` tests pass by design — every function starts with `NotImplementedError`
  or intentionally buggy code
- `complete/` tests pass 100%

## Error Handling Philosophy

- Tutorial code uses explicit error types from standard library (`ValueError`, `TypeError`,
  `NotImplementedError`)
- No custom exception hierarchies in `initial/` or `complete/` (keeps focus on learning,
  not project scaffolding)
- Tests assert on specific exception types and messages where relevant to the concept

## Implementation Order

Modules build concepts progressively. Recommended build order is the same as learning
order (01 → 08), but each module is self-contained after build. Implementation follows
the TDD principle: write `test_practice.py` first, then `complete/practice.py`, then
`initial/practice.py` (strip implementations), then `tutorial.ipynb`.
