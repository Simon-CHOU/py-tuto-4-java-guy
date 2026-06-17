"""Root-level command for running a single exercise by question ID."""

import argparse
import importlib.util
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from scripts.exercise_registry import ExerciseSpec, get_exercise

ROOT = Path(__file__).resolve().parent.parent
VALID_TARGETS = ("initial", "complete")

STATUS_PASSED = "PASSED"
STATUS_NOT_STARTED = "NOT_STARTED"
STATUS_IN_PROGRESS = "IN_PROGRESS"
STATUS_BLOCKED = "BLOCKED"
STATUS_ENVIRONMENT_ERROR = "ENVIRONMENT_ERROR"
STATUS_LOAD_ERROR = "LOAD_ERROR"
STATUS_RUNNER_ERROR = "RUNNER_ERROR"

STATUS_LABELS = {
    STATUS_PASSED: "PASSED",
    STATUS_NOT_STARTED: "NOT STARTED",
    STATUS_IN_PROGRESS: "IN PROGRESS",
    STATUS_BLOCKED: "BLOCKED",
    STATUS_ENVIRONMENT_ERROR: "ENVIRONMENT ERROR",
    STATUS_LOAD_ERROR: "LOAD ERROR",
    STATUS_RUNNER_ERROR: "RUNNER ERROR",
}

SUMMARY_STATUS_LABELS = {
    STATUS_PASSED: "PASS",
    STATUS_NOT_STARTED: "NOT_STARTED",
    STATUS_IN_PROGRESS: "IN_PROGRESS",
    STATUS_BLOCKED: "BLOCKED",
    STATUS_ENVIRONMENT_ERROR: "ENV_ERROR",
    STATUS_LOAD_ERROR: "LOAD_ERROR",
    STATUS_RUNNER_ERROR: "RUNNER_ERROR",
}

LOAD_ERROR_MARKERS = (
    "ERROR collecting",
    "ImportError while importing test module",
    "SyntaxError:",
    "IndentationError:",
)


@dataclass(frozen=True, slots=True)
class ExerciseRunResult:
    exercise: ExerciseSpec
    target: str
    status: str
    reason: str
    meaning: str
    next_steps: tuple[str, ...]
    returncode: int
    raw_output: str = ""

    @property
    def summary_status(self) -> str:
        return SUMMARY_STATUS_LABELS[self.status]

    @property
    def display_status(self) -> str:
        return STATUS_LABELS[self.status]


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


def practice_file_for(exercise: ExerciseSpec, target: str) -> Path:
    return ROOT / exercise.module_dir / target / "practice.py"


def pytest_is_available() -> bool:
    return importlib.util.find_spec("pytest") is not None


def has_todo_placeholder(exercise: ExerciseSpec, target: str) -> bool:
    practice_file = practice_file_for(exercise, target)
    marker = f'TODO: implement {exercise.symbol_name}'
    return practice_file.exists() and marker in practice_file.read_text(encoding="utf-8")


def _default_next_steps(exercise: ExerciseSpec, target: str) -> tuple[str, ...]:
    practice_file = practice_file_for(exercise, target)
    return (
        f"Open {practice_file.relative_to(ROOT)}.",
        f"Implement `{exercise.symbol_name}`.",
        f"Run `uv run learn {exercise.question_id}` again.",
    )


def _combined_output(result: subprocess.CompletedProcess[str]) -> str:
    stdout = result.stdout or ""
    stderr = result.stderr or ""
    return "\n".join(part for part in (stdout.strip(), stderr.strip()) if part).strip()


def _looks_like_load_error(output: str) -> bool:
    return any(marker in output for marker in LOAD_ERROR_MARKERS)


def _blocked_todo_symbol(output: str, current_symbol: str) -> str | None:
    match = re.search(r"TODO: implement (?P<symbol>[A-Za-z_][A-Za-z0-9_]*)", output)
    if match is None:
        return None
    blocked_symbol = match.group("symbol")
    if blocked_symbol == current_symbol:
        return None
    return blocked_symbol


def evaluate_exercise(exercise: ExerciseSpec, target: str) -> ExerciseRunResult:
    if not pytest_is_available():
        return ExerciseRunResult(
            exercise=exercise,
            target=target,
            status=STATUS_ENVIRONMENT_ERROR,
            reason="`pytest` is not installed in the current project environment.",
            meaning="This is an environment problem, not a problem with your solution.",
            next_steps=(
                "Run `uv sync --extra dev` in the project root.",
                f"Run `uv run learn {exercise.question_id}` again.",
            ),
            returncode=1,
        )

    if has_todo_placeholder(exercise, target):
        return ExerciseRunResult(
            exercise=exercise,
            target=target,
            status=STATUS_NOT_STARTED,
            reason=f"`{exercise.symbol_name}` still contains its TODO placeholder implementation.",
            meaning="You have not started this exercise yet.",
            next_steps=_default_next_steps(exercise, target),
            returncode=1,
        )

    completed = run_exercise(exercise, target, capture_output=True)
    output = _combined_output(completed)

    if completed.returncode == 0:
        return ExerciseRunResult(
            exercise=exercise,
            target=target,
            status=STATUS_PASSED,
            reason="All checks for this exercise passed.",
            meaning="Your current implementation matches the exercise expectations.",
            next_steps=(
                "Move on to the next question, or run `uv run summary` to see overall progress.",
            ),
            returncode=0,
            raw_output=output,
        )

    blocked_symbol = _blocked_todo_symbol(output, exercise.symbol_name)
    if blocked_symbol is not None:
        return ExerciseRunResult(
            exercise=exercise,
            target=target,
            status=STATUS_BLOCKED,
            reason=(
                f"The module cannot be imported yet because `{blocked_symbol}` still has a TODO "
                "placeholder."
            ),
            meaning="This exercise is blocked by another unfinished TODO in the same module.",
            next_steps=(
                f"Open {practice_file_for(exercise, target).relative_to(ROOT)}.",
                (
                    f"Implement `{blocked_symbol}` first, or switch to its question "
                    f"before returning to `{exercise.symbol_name}`."
                ),
                f"Run `uv run learn {exercise.question_id}` again.",
            ),
            returncode=completed.returncode,
            raw_output=output,
        )

    if _looks_like_load_error(output):
        return ExerciseRunResult(
            exercise=exercise,
            target=target,
            status=STATUS_LOAD_ERROR,
            reason="Python could not import or parse your code before the tests could run.",
            meaning="This is a code-loading problem, such as a syntax or import error.",
            next_steps=(
                (
                    f"Open {practice_file_for(exercise, target).relative_to(ROOT)} "
                    "and fix the import or syntax issue."
                ),
                (
                    f"Run `uv run learn {exercise.question_id} --verbose` "
                    "to inspect the raw pytest details."
                ),
            ),
            returncode=completed.returncode,
            raw_output=output,
        )

    return ExerciseRunResult(
        exercise=exercise,
        target=target,
        status=STATUS_IN_PROGRESS,
        reason="The tests ran, but at least one expected behavior is still failing.",
        meaning="You have started the exercise, but the implementation is not correct yet.",
        next_steps=(
            "Fix the behavior described by the failing test.",
            (
                f"Run `uv run learn {exercise.question_id} --verbose` "
                "for the raw pytest failure details."
            ),
        ),
        returncode=completed.returncode,
        raw_output=output,
    )


def render_exercise_result(result: ExerciseRunResult, *, verbose: bool) -> str:
    module_name = Path(result.exercise.module_dir).name
    lines = [
        f"Question: {result.exercise.question_id}",
        f"Topic: {module_name}",
        f"Task: {result.exercise.symbol_name}",
        f"Target: {result.target}",
        "",
        f"Status: {result.display_status}",
        f"Meaning: {result.meaning}",
        f"Reason: {result.reason}",
        "",
        "Next step:",
    ]
    for index, step in enumerate(result.next_steps, start=1):
        lines.append(f"{index}. {step}")

    if verbose and result.raw_output:
        lines.extend(("", "Raw pytest output:", result.raw_output))

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one exercise by question ID.")
    parser.add_argument("question_id", help="Question ID like M01-Q01")
    parser.add_argument(
        "--target",
        choices=VALID_TARGETS,
        default="initial",
        help="Which implementation target to test",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show the raw pytest output after the learner-friendly summary.",
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

    result = evaluate_exercise(exercise, args.target)
    print(render_exercise_result(result, verbose=args.verbose), flush=True)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
