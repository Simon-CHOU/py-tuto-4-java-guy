"""Module 08: Concurrency and Parallelism — Reference Implementation."""

import concurrent.futures
import math
import threading
import time


def sequential_sum(iterable):
    return sum(iterable)


def _chunked_sum(args):
    data_slice, start, end = args
    return sum(data_slice[start:end])


def _make_chunks(data, num_chunks):
    n = len(data)
    chunk_size = math.ceil(n / num_chunks)
    chunks = []
    for i in range(0, n, chunk_size):
        chunks.append((data, i, min(i + chunk_size, n)))
    return chunks


def threaded_sum(iterable, num_threads=4):
    data = list(iterable)
    chunks = _make_chunks(data, num_threads)
    total = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for result in executor.map(_chunked_sum, chunks):
            total += result
    return total


def process_sum(iterable, num_processes=4):
    data = list(iterable)
    chunks = _make_chunks(data, num_processes)
    total = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        for result in executor.map(_chunked_sum, chunks):
            total += result
    return total


def _cpu_heavy_work():
    total = 0
    for i in range(5_000_000):
        total += i
    return total


def gil_demonstration():
    start = time.perf_counter()
    for _ in range(4):
        _cpu_heavy_work()
    sequential_time = time.perf_counter() - start

    start = time.perf_counter()
    threads = []
    for _ in range(4):
        t = threading.Thread(target=_cpu_heavy_work)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    threaded_time = time.perf_counter() - start

    return {
        "sequential_time": sequential_time,
        "threaded_time": threaded_time,
    }


def countdown(n):
    return list(range(n, 0, -1)) + ["go!"]
