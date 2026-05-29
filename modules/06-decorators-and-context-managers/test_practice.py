"""Tests for Module 06: Decorators and Context Managers."""
import os
import sys
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

import pytest
from practice import timer, retry, memoize, TimedOpen, validate_types


class TestTimer:
    def test_returns_result(self):
        @timer
        def slow_add(a, b):
            time.sleep(0.01)
            return a + b

        result = slow_add(1, 2)
        assert result == 3

    def test_preserves_metadata(self):
        @timer
        def documented_func():
            """Docstring here."""
            pass

        assert documented_func.__name__ == "documented_func"
        assert documented_func.__doc__ == "Docstring here."


class TestRetry:
    def test_succeeds_first_try(self):
        call_count = 0

        @retry(max_attempts=3, exceptions=(ValueError,))
        def maybe_fail():
            nonlocal call_count
            call_count += 1
            return "ok"

        result = maybe_fail()
        assert result == "ok"
        assert call_count == 1

    def test_retries_on_exception(self):
        call_count = 0

        @retry(max_attempts=3, exceptions=(ValueError,))
        def fails_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("transient error")
            return "recovered"

        result = fails_twice()
        assert result == "recovered"
        assert call_count == 3

    def test_exhausts_retries(self):
        @retry(max_attempts=2, exceptions=(ValueError,))
        def always_fails():
            raise ValueError("persistent error")

        with pytest.raises(ValueError, match="persistent error"):
            always_fails()


class TestMemoize:
    def test_caches_results(self):
        call_count = 0

        @memoize
        def expensive(n):
            nonlocal call_count
            call_count += 1
            return n * 2

        assert expensive(5) == 10
        assert expensive(5) == 10
        assert call_count == 1

    def test_different_args(self):
        @memoize
        def add(a, b):
            return a + b

        assert add(1, 2) == 3
        assert add(2, 3) == 5


class TestTimedOpen:
    def test_writes_and_reads(self, tmp_path):
        filepath = tmp_path / "test.txt"
        with TimedOpen(filepath, "w") as f:
            f.write("hello")

        assert filepath.read_text() == "hello"

    def test_file_closed_after_with(self, tmp_path):
        filepath = tmp_path / "test.txt"
        with TimedOpen(filepath, "w") as f:
            f.write("data")

        assert f.closed is True


class TestValidateTypes:
    def test_valid_types(self):
        @validate_types
        def greet(name: str, times: int) -> str:
            return name * times

        assert greet("hi", 3) == "hihihi"

    def test_invalid_type_raises(self):
        @validate_types
        def greet(name: str, times: int) -> str:
            return name * times

        with pytest.raises(TypeError):
            greet("hi", "not_an_int")

    def test_no_annotations_passes(self):
        @validate_types
        def no_hints(a, b):
            return a + b

        assert no_hints(1, 2) == 3
