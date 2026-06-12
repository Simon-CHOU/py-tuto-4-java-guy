"""Module 09: asyncio — Your Implementation."""


async def async_fetch_all(urls: list[str], delay: float = 0.1) -> list[str]:
    """Simulate concurrent async HTTP fetches.

    Use asyncio.sleep(delay) to simulate network latency per URL.
    Return a list like ["data_http://a.com", "data_http://b.com"].

    Java analogy: CompletableFuture.supplyAsync() + CompletableFuture.allOf()
    Key difference: async/await is cooperative, not threaded — no context switching overhead.

    Hint: Use asyncio.gather() to run all tasks concurrently.
    """
    raise NotImplementedError("TODO: implement async_fetch_all")


async def async_countdown(n: int):
    """Async generator that counts down from n to 1, sleeping 0.05s between each.

    Yields integers: n, n-1, ..., 1.
    Use 'async for' to consume this generator.

    Java analogy: Reactive Streams (Flux.range().delayElements())
    Python async generators combine 'async def' + 'yield' — one of Python's most
    distinctive concurrency features with no Java equivalent.
    """
    raise NotImplementedError("TODO: implement async_countdown")


async def run_concurrently(*coros):
    """Run multiple coroutines concurrently and return results in order.

    Must use asyncio.gather() — this is the core primitive for running
    async tasks in parallel (cooperatively, not OS threads).

    Java analogy: CompletableFuture.allOf(futures).join()
    """
    raise NotImplementedError("TODO: implement run_concurrently")


async def async_timer(coro) -> tuple[float, object]:
    """Wrap a coroutine, measure its wall-clock time. Return (elapsed, result).

    Use time.perf_counter() before and after awaiting the coroutine.

    Java analogy: Measuring CompletableFuture.get() duration.
    """
    raise NotImplementedError("TODO: implement async_timer")
