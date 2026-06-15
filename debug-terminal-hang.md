# Debug Session: terminal-hang

Status: RESOLVED

## Scope

Investigate terminal hangs observed while verifying the new root-level CLI commands.

## Hypotheses

1. The local `.venv` uses the wrong Python version for this project.
2. `uv venv` is blocking on an interactive confirmation prompt.
3. Residual `uv` / `uvx` / `python` child processes are left running after failed commands.
4. The CLI commands fail because the active environment is missing `pytest` and other dev dependencies.

## Evidence Log

- The original local `.venv` was invalid for this project:
  - `pyproject.toml` requires Python `>=3.12`
  - the local `.venv` reported Python `3.10.11`
  - `python.exe` existed but `pyvenv.cfg` was missing after a failed rebuild
- `uv venv --python 3.12 .venv` blocked because an existing `.venv` triggered an interactive confirmation prompt.
- Heavy `uv pip install -e ".[dev]"` runs in the sandbox were interrupted mid-flight, leaving partially installed environments and broken `dist-info` metadata.
- Console script validation exposed a packaging bug:
  - `learn.exe`, `summary.exe`, and `test-all.exe` all failed with `ModuleNotFoundError: No module named 'scripts'`
  - adding `scripts/__init__.py` alone was not enough
  - explicit setuptools package declaration in `pyproject.toml` was required

## Root Cause

The terminal hang symptom was caused by a stack of environment and packaging issues, not by the new CLI business logic:

1. a stale/incompatible `.venv`
2. interactive `uv venv` confirmation in a non-interactive sandbox
3. interrupted long-running dependency installation
4. missing package discovery for the `scripts` package

## Fix

- Added `scripts/__init__.py`
- Added explicit setuptools packaging config in `pyproject.toml`
- Verified commands in a clean Python 3.12 environment with minimal required dependencies

## Verification

- `learn.exe M01-Q01 --target complete` passed
- `summary.exe --target complete` reported `45 / 45` passing
- `test-all.exe` still reported `All modules passed`
- default learner path `learn.exe M01-Q01` correctly failed against `initial/` implementation
