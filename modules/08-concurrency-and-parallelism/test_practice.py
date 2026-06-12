# ruff: noqa: E402 — sys.path must be set before imports; conftest.py fixes this in P1
"""Tests for Module 08: Concurrency and Parallelism."""

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

from practice import (
    countdown,
    gil_demonstration,
    process_sum,
    sequential_sum,
    threaded_sum,
)


class TestSequentialSum:
    def test_sum_range(self):
        assert sequential_sum(range(1, 101)) == 5050

    def test_empty(self):
        assert sequential_sum([]) == 0


class TestThreadedSum:
    def test_sum_range_2_threads(self):
        result = threaded_sum(range(1, 101), num_threads=2)
        assert result == 5050

    def test_sum_range_4_threads(self):
        result = threaded_sum(range(1, 101), num_threads=4)
        assert result == 5050


class TestProcessSum:
    def test_sum_range(self):
        result = process_sum(range(1, 101), num_processes=2)
        assert result == 5050


class TestGILDemonstration:
    def test_returns_dict_with_expected_keys(self):
        result = gil_demonstration()
        assert "sequential_time" in result
        assert "threaded_time" in result
        assert isinstance(result["sequential_time"], float)
        assert isinstance(result["threaded_time"], float)


class TestCountdown:
    def test_returns_list(self):
        result = countdown(3)
        assert result == [3, 2, 1, "go!"]
