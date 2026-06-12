"""Run all module tests against the complete implementation."""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def main():
    modules = sorted(HERE.glob("modules/*/run_test.py"))
    failures = 0
    for run_script in modules:
        name = run_script.parent.name
        print(f"\n=== {name} ===")
        result = subprocess.run(
            [sys.executable, str(run_script), "complete"],
            cwd=run_script.parent,
        )
        if result.returncode != 0:
            failures += 1
    if failures:
        print(f"\n{failures} module(s) failed")
    else:
        print("\nAll modules passed")
    sys.exit(failures)


if __name__ == "__main__":
    main()
