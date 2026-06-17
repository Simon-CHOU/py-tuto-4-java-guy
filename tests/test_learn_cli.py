import subprocess

from scripts.exercise_registry import get_exercise
from scripts.learn import (
    STATUS_BLOCKED,
    STATUS_ENVIRONMENT_ERROR,
    STATUS_IN_PROGRESS,
    STATUS_LOAD_ERROR,
    STATUS_NOT_STARTED,
    STATUS_PASSED,
    evaluate_exercise,
    render_exercise_result,
)


def test_evaluate_exercise_reports_not_started_without_running_pytest(monkeypatch):
    exercise = get_exercise("M01-Q01")

    monkeypatch.setattr("scripts.learn.pytest_is_available", lambda: True)
    monkeypatch.setattr(
        "scripts.learn.run_exercise",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("pytest should not run")),
    )

    result = evaluate_exercise(exercise, "initial")

    assert result.status == STATUS_NOT_STARTED
    assert "not started" in result.meaning.lower()
    assert "TODO placeholder" in result.reason


def test_evaluate_exercise_reports_environment_error_when_pytest_is_missing(monkeypatch):
    exercise = get_exercise("M01-Q01")

    monkeypatch.setattr("scripts.learn.pytest_is_available", lambda: False)

    result = evaluate_exercise(exercise, "initial")

    assert result.status == STATUS_ENVIRONMENT_ERROR
    assert "environment problem" in result.meaning.lower()
    assert "uv sync --extra dev" in result.next_steps[0]


def test_evaluate_exercise_reports_passed(monkeypatch):
    exercise = get_exercise("M01-Q01")

    monkeypatch.setattr("scripts.learn.pytest_is_available", lambda: True)
    monkeypatch.setattr("scripts.learn.has_todo_placeholder", lambda *args, **kwargs: False)
    monkeypatch.setattr(
        "scripts.learn.run_exercise",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=["pytest"], returncode=0, stdout="7 passed", stderr=""
        ),
    )

    result = evaluate_exercise(exercise, "initial")

    assert result.status == STATUS_PASSED
    assert result.summary_status == "PASS"


def test_evaluate_exercise_reports_load_error(monkeypatch):
    exercise = get_exercise("M01-Q01")

    monkeypatch.setattr("scripts.learn.pytest_is_available", lambda: True)
    monkeypatch.setattr("scripts.learn.has_todo_placeholder", lambda *args, **kwargs: False)
    monkeypatch.setattr(
        "scripts.learn.run_exercise",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=["pytest"],
            returncode=2,
            stdout="ERROR collecting test_practice.py\nSyntaxError: invalid syntax",
            stderr="",
        ),
    )

    result = evaluate_exercise(exercise, "initial")

    assert result.status == STATUS_LOAD_ERROR
    assert "syntax or import error" in result.meaning.lower()


def test_evaluate_exercise_reports_blocked_when_another_todo_breaks_import(monkeypatch):
    exercise = get_exercise("M03-Q01")

    monkeypatch.setattr("scripts.learn.pytest_is_available", lambda: True)
    monkeypatch.setattr("scripts.learn.has_todo_placeholder", lambda *args, **kwargs: False)
    monkeypatch.setattr(
        "scripts.learn.run_exercise",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=["pytest"],
            returncode=4,
            stdout='E   NotImplementedError: TODO: implement BetterDict',
            stderr="",
        ),
    )

    result = evaluate_exercise(exercise, "initial")

    assert result.status == STATUS_BLOCKED
    assert "betterdict" in result.reason.lower()
    assert "blocked by another unfinished todo" in result.meaning.lower()


def test_evaluate_exercise_reports_in_progress(monkeypatch):
    exercise = get_exercise("M01-Q01")

    monkeypatch.setattr("scripts.learn.pytest_is_available", lambda: True)
    monkeypatch.setattr("scripts.learn.has_todo_placeholder", lambda *args, **kwargs: False)
    monkeypatch.setattr(
        "scripts.learn.run_exercise",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=["pytest"],
            returncode=1,
            stdout="FAILED test_practice.py::TestClassifyNumber::test_zero",
            stderr="",
        ),
    )

    result = evaluate_exercise(exercise, "initial")

    assert result.status == STATUS_IN_PROGRESS
    assert "started the exercise" in result.meaning.lower()


def test_render_exercise_result_hides_raw_output_by_default(monkeypatch):
    exercise = get_exercise("M01-Q01")

    monkeypatch.setattr("scripts.learn.pytest_is_available", lambda: True)
    monkeypatch.setattr("scripts.learn.has_todo_placeholder", lambda *args, **kwargs: False)
    monkeypatch.setattr(
        "scripts.learn.run_exercise",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=["pytest"],
            returncode=1,
            stdout="FAILED test_practice.py::TestClassifyNumber::test_zero",
            stderr="",
        ),
    )

    result = evaluate_exercise(exercise, "initial")
    rendered = render_exercise_result(result, verbose=False)

    assert "Status: IN PROGRESS" in rendered
    assert "Raw pytest output:" not in rendered


def test_render_exercise_result_includes_raw_output_in_verbose_mode(monkeypatch):
    exercise = get_exercise("M01-Q01")

    monkeypatch.setattr("scripts.learn.pytest_is_available", lambda: True)
    monkeypatch.setattr("scripts.learn.has_todo_placeholder", lambda *args, **kwargs: False)
    monkeypatch.setattr(
        "scripts.learn.run_exercise",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=["pytest"],
            returncode=1,
            stdout="FAILED test_practice.py::TestClassifyNumber::test_zero",
            stderr="",
        ),
    )

    result = evaluate_exercise(exercise, "initial")
    rendered = render_exercise_result(result, verbose=True)

    assert "Raw pytest output:" in rendered
    assert "FAILED test_practice.py::TestClassifyNumber::test_zero" in rendered
