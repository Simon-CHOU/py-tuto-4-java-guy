"""Root-level command for running a single exercise by question ID."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

from scripts.exercise_registry import ExerciseSpec, get_exercise

ROOT = Path(__file__).resolve().parent.parent
VALID_TARGETS = ("initial", "complete")


def run_exercise(
    exercise: ExerciseSpec,
    target: str,
    *,
    capture_output: bool,
) -> subprocess.CompletedProcess[str]:
    module_path = ROOT / exercise.module_dir
    command = [
        sys.executable,
        "-m",
        "pytest",
        f"test_practice.py::{exercise.pytest_class_name}",
        "-v",
    ]
    kwargs: dict[str, object] = {
        "cwd": str(module_path),
        "env": {**os.environ, "PRACTICE_TARGET": target},
        "text": True,
    }
    if capture_output:
        kwargs["capture_output"] = True
    return subprocess.run(command, **kwargs)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one exercise by question ID.")
    parser.add_argument("question_id", help="Question ID like M01-Q01")
    parser.add_argument(
        "--target",
        choices=VALID_TARGETS,
        default="initial",
        help="Which implementation target to test",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    question_id = args.question_id.upper()
    try:
        exercise = get_exercise(question_id)
    except KeyError:
        print(f"Unknown question ID: {question_id}", file=sys.stderr)
        return 1

    module_name = Path(exercise.module_dir).name
    print(f"[{exercise.question_id}] {module_name} :: {exercise.symbol_name}")
    result = run_exercise(exercise, args.target, capture_output=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
