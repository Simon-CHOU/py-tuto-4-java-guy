"""Root-level command for summarizing exercise progress."""

import argparse
from collections import defaultdict
from pathlib import Path

from scripts.exercise_registry import list_exercises
from scripts.learn import STATUS_PASSED, VALID_TARGETS, evaluate_exercise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize progress for all exercises.")
    parser.add_argument(
        "--target",
        choices=VALID_TARGETS,
        default="initial",
        help="Which implementation target to test",
    )
    return parser.parse_args()


def _format_progress(passed: int, total: int) -> str:
    if total == 0:
        return "0%"
    return f"{round(passed * 100 / total):.0f}%"


def _print_question_table(rows: list[tuple[str, str, str, str]]) -> None:
    headers = ("Question ID", "Module", "Symbol", "Status")
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    print(" | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    for row in rows:
        print(" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)))


def _print_module_table(rows: list[tuple[str, str, str, str]]) -> None:
    headers = ("Module", "Passed", "Total", "Progress")
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    print()
    print(" | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    for row in rows:
        print(" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)))


def main() -> int:
    args = parse_args()
    question_rows: list[tuple[str, str, str, str]] = []
    module_totals: dict[str, dict[str, int]] = defaultdict(lambda: {"passed": 0, "total": 0})
    failures = 0

    for exercise in list_exercises():
        result = evaluate_exercise(exercise, args.target)
        module_name = Path(exercise.module_dir).name
        status = result.summary_status
        question_rows.append((exercise.question_id, module_name, exercise.symbol_name, status))
        module_totals[module_name]["total"] += 1
        if result.status == STATUS_PASSED:
            module_totals[module_name]["passed"] += 1
        else:
            failures += 1

    module_rows: list[tuple[str, str, str, str]] = []
    total_passed = 0
    total_questions = 0
    for module_name in sorted(module_totals):
        passed = module_totals[module_name]["passed"]
        total = module_totals[module_name]["total"]
        total_passed += passed
        total_questions += total
        module_rows.append((module_name, str(passed), str(total), _format_progress(passed, total)))
    module_rows.append(
        (
            "TOTAL",
            str(total_passed),
            str(total_questions),
            _format_progress(total_passed, total_questions),
        )
    )

    _print_question_table(question_rows)
    _print_module_table(module_rows)
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
