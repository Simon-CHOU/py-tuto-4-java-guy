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
