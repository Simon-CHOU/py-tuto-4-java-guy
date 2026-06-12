"""Module 09: asyncio — Reference Implementation."""

import asyncio
import time


async def async_fetch_all(urls: list[str], delay: float = 0.1) -> list[str]:
    async def _fetch(url: str) -> str:
        await asyncio.sleep(delay)
        return f"data_{url}"

    tasks = [_fetch(url) for url in urls]
    return await asyncio.gather(*tasks)


async def async_countdown(n: int):
    for i in range(n, 0, -1):
        await asyncio.sleep(0.05)
        yield i


async def run_concurrently(*coros):
    return await asyncio.gather(*coros)


async def async_timer(coro) -> tuple[float, object]:
    start = time.perf_counter()
    result = await coro
    elapsed = time.perf_counter() - start
    return (elapsed, result)
