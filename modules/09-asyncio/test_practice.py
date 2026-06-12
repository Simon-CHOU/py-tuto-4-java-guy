# ruff: noqa: E402 — sys.path must be set before imports; conftest.py fixes this in P1
"""Tests for Module 09: asyncio."""

import asyncio
import os
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
target = HERE / os.environ.get("PRACTICE_TARGET", "complete")
sys.path.insert(0, str(target))

from practice import async_countdown, async_fetch_all, async_timer, run_concurrently


class TestAsyncFetchAll:
    @pytest.mark.asyncio
    async def test_single_url(self):
        result = await async_fetch_all(["http://a.com"], delay=0.01)
        assert result == ["data_http://a.com"]

    @pytest.mark.asyncio
    async def test_multiple_urls(self):
        urls = ["http://a.com", "http://b.com", "http://c.com"]
        result = await async_fetch_all(urls, delay=0.01)
        assert len(result) == 3
        for url in urls:
            assert f"data_{url}" in result

    @pytest.mark.asyncio
    async def test_empty_list(self):
        result = await async_fetch_all([], delay=0.01)
        assert result == []

    @pytest.mark.asyncio
    async def test_order_preserved(self):
        urls = ["http://first.com", "http://second.com"]
        result = await async_fetch_all(urls, delay=0.01)
        assert result == ["data_http://first.com", "data_http://second.com"]


class TestAsyncCountdown:
    @pytest.mark.asyncio
    async def test_yields_correct_sequence(self):
        result = []
        async for value in async_countdown(3):
            result.append(value)
        assert result == [3, 2, 1]

    @pytest.mark.asyncio
    async def test_is_async_generator(self):
        import inspect

        assert inspect.isasyncgen(async_countdown(3))


class TestRunConcurrently:
    @pytest.mark.asyncio
    async def test_runs_all_coroutines(self):
        async def one():
            await asyncio.sleep(0.01)
            return 1

        async def two():
            return 2

        result = await run_concurrently(one(), two())
        assert result == [1, 2]

    @pytest.mark.asyncio
    async def test_empty_call(self):
        result = await run_concurrently()
        assert result == []


class TestAsyncTimer:
    @pytest.mark.asyncio
    async def test_returns_tuple(self):
        async def work():
            await asyncio.sleep(0.01)
            return 42

        elapsed, result = await async_timer(work())
        assert isinstance(elapsed, float)
        assert elapsed > 0
        assert result == 42
