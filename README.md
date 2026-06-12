# Python Tutorial for Java Developers

A hands-on Python tutorial for Java developers preparing for a Python-related role. Built around the principle: **new knowledge attaches best to existing knowledge** — every module starts from a familiar Java concept and maps it to the Python equivalent.

**Goal:** Build enough Python awareness to answer common interview questions confidently and close the gap between "I've read about Python" and "I can write Python."

## Quick Start (Handbook)

### 1. Install `uv` — Python's SDKMAN + Maven

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# WSL2 / Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and set up the project

```bash
git clone <this-repo>
cd py-tuto-4-java-guy

uv python install 3.14      # Install Python (like sdk install java 21)
uv venv                      # Create virtualenv (like a project-local JAVA_HOME)
source .venv/bin/activate    # WSL2/Linux
# or
.venv\Scripts\activate       # Windows PowerShell

uv pip install -e ".[dev]"   # Install dev tools (pytest, jupyter)
```

### 3. Work through a module

Each module follows the same flow:

```bash
cd modules/01-basics-and-types

# Step 1: See the tests you need to pass (they'll all fail)
python run_test.py initial

# Step 2: Open initial/practice.py — fill in the blanks
# Step 3: Run tests again until they pass
python run_test.py initial

# Step 4: Compare with the reference answer
python run_test.py complete

# Step 5: Study the Java ↔ Python comparison
jupyter notebook tutorial.ipynb
# Or open in VS Code / any .ipynb viewer
```

### 4. Run all tests

```bash
# Run each module's tests against the reference answers
for d in modules/*/; do (cd "$d" && python run_test.py complete); done
```

## Mental Model: Java → Python at a Glance

| When you think... | Python does... |
|---|---|
| `javac Foo.java && java Foo` | `python foo.py` (compiled to .pyc automatically, cached in `__pycache__/`) |
| `pom.xml` / `build.gradle` | `pyproject.toml` + `uv` (or `pip`) |
| `~/.m2/repository` | `site-packages/` inside each virtualenv |
| `CLASSPATH` | `sys.path` (list of directories, modifiable at runtime) |
| `package com.foo;` | Directory structure IS the package (no declaration needed) |
| `import com.foo.Bar;` | `from foo import Bar` or `import foo.bar` |
| `interface Foo { }` | `ABC` + `@abstractmethod` or `Protocol` or duck typing |
| `@Override` | Not needed (everything is virtual) |
| `private` | Convention: prefix with `_` (not enforced) |
| `getX()` / `setX()` | `@property` — transparent attribute access |
| `new ArrayList<>()` | `[]` (list), `{}` (dict), `set()` (set) |
| `stream().filter().map().collect()` | `[f(x) for x in seq if p(x)]` |
| `Thread` for CPU work | `ProcessPoolExecutor` (GIL prevents thread parallelism) |
| `CompletableFuture` | `asyncio` + `async`/`await` |
| `try-with-resources` | `with` statement (context manager protocol) |
| `instanceof` | `isinstance(x, Type)` |
| `null` | `None` (singleton, has type `NoneType`) |
| `String.format()` | f-strings: `f"Hello {name}"` |
| `record` (Java 14+) | `@dataclass` |

## Modules

| # | Topic | The interview question it answers |
|---|-------|-----------------------------------|
| 01 | **Basics and Types** | "Everything's an object? Even `int`?" |
| 02 | **Functional Features** | "How do you do streams/filter/map without Stream API?" |
| 03 | **OOP** | "No private? No overloading? How does OOP even work?" |
| 04 | **Interfaces and Abstraction** | "No `interface` keyword — how do I express a contract?" |
| 05 | **Modules and Packages** | "No maven, no classpath — how do you organize code?" |
| 06 | **Decorators and Context Managers** | "Are decorators like Java annotations?" (Spoiler: no) |
| 07 | **Type Hints** | "Can Python types give me real type safety?" |
| 08 | **Concurrency and Parallelism** | "What's the GIL, and how do I run CPU work in parallel?" |
| 09 | **asyncio** | "How do you handle concurrent I/O without threads?" |

Each module contains:
- `tutorial.ipynb` — interactive notebook comparing Java and Python
- `initial/practice.py` — skeleton code you fill in (with hints)
- `complete/practice.py` — reference implementation
- `test_practice.py` — shared test suite (pytest)
- `run_test.py` — cross-platform test runner

## Project Structure

```
py-tuto-4-java-guy/
├── pyproject.toml              # Project config (uv + pytest)
├── modules/
│   ├── 01-basics-and-types/
│   │   ├── tutorial.ipynb
│   │   ├── initial/practice.py   # ← You work here
│   │   ├── complete/practice.py  # ← Reference answer
│   │   ├── test_practice.py
│   │   └── run_test.py           # python run_test.py initial|complete
│   ├── 02-functional-features/
│   ├── 03-oop/
│   ├── 04-interfaces-and-abstraction/
│   ├── 05-modules-and-packages/
│   ├── 06-decorators-and-context-managers/
│   ├── 07-type-hints/
│   └── 08-concurrency-and-parallelism/
│   └── 09-asyncio/
└── docs/
    ├── python-3.14-docs-html/   # Offline Python docs
    └── superpowers/             # Design spec & implementation plan
```

## Key Python Facts for Interviews

**GIL (Global Interpreter Lock):** A mutex that prevents multiple threads from executing Python bytecode simultaneously. Exists because CPython uses reference counting for memory management. Released during I/O operations. Being addressed in Python 3.13+ (free-threaded build via PEP 703).

**Parallelism without third-party libs (3 approaches):**
1. `multiprocessing` / `ProcessPoolExecutor` — separate processes, each with own GIL (for CPU-bound)
2. `ThreadPoolExecutor` — threads for I/O-bound (GIL released during I/O)
3. `asyncio` — cooperative multitasking for high-concurrency I/O

**Interfaces in Python (3 approaches):**
1. `ABC` + `@abstractmethod` — most Java-like, enforced at instantiation time
2. `Protocol` — structural subtyping, checked by mypy (like Go interfaces)
3. Duck typing — just call the method, trust it's there (most Pythonic)

## Requirements

- Python 3.12+
- `uv` (Python package manager)
- The tutorial code itself uses **zero third-party dependencies** — standard library only

## References

- [Python 3.14 Documentation](https://docs.python.org/3/) (offline copy in `docs/`)
- [Learn Python in Y Minutes](https://learnxinyminutes.com/python/)
