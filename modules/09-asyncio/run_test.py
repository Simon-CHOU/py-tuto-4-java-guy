"""Run tests for module 09 against initial/ or complete/ implementation."""

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def show_diff():
    """Show unified diff between initial/ and complete/ practice.py."""
    import difflib

    initial = HERE / "initial" / "practice.py"
    complete = HERE / "complete" / "practice.py"
    if not initial.exists() or not complete.exists():
        print("Cannot diff: missing initial/ or complete/ practice.py", file=sys.stderr)
        sys.exit(1)
    diff = difflib.unified_diff(
        initial.read_text().splitlines(keepends=True),
        complete.read_text().splitlines(keepends=True),
        fromfile="initial/practice.py",
        tofile="complete/practice.py",
    )
    sys.stdout.writelines(diff)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("initial", "complete", "diff"):
        print("Usage: python run_test.py initial|complete|diff", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "diff":
        show_diff()
        sys.exit(0)

    env = {**os.environ, "PRACTICE_TARGET": sys.argv[1]}
    args = [sys.executable, "-m", "pytest", str(HERE / "test_practice.py"), "-v"]
    result = subprocess.run(args, env=env, cwd=str(HERE))
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
