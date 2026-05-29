"""Module 08: Concurrency and Parallelism — Your Implementation."""


def sequential_sum(iterable):
    """Sum an iterable in a single thread. This is the baseline.

    Just use the built-in sum() function.
    """
    raise NotImplementedError("TODO: implement sequential_sum")


def threaded_sum(iterable, num_threads=4):
    """Sum using threading.Thread or ThreadPoolExecutor.

    KEY INSIGHT: Due to the GIL, this will NOT be faster than sequential_sum
    for CPU-bound work. Only one thread executes Python bytecode at a time.

    For I/O-bound work (reading files, network requests), threads ARE useful
    because the GIL is released during I/O operations.

    Use concurrent.futures.ThreadPoolExecutor.
    """
    raise NotImplementedError("TODO: implement threaded_sum")


def process_sum(iterable, num_processes=4):
    """Sum using multiprocessing. Each process has its own Python interpreter + GIL.

    This IS truly parallel for CPU-bound work. The cost: spawning processes is
    expensive (pickle serialization, memory copy on some platforms).

    Use concurrent.futures.ProcessPoolExecutor.
    """
    raise NotImplementedError("TODO: implement process_sum")


def _cpu_heavy_work():
    """Simulate CPU-bound computation."""
    total = 0
    for i in range(5_000_000):
        total += i
    return total


def gil_demonstration():
    """Demonstrate GIL impact: compare sequential vs threaded for CPU work.

    Run _cpu_heavy_work() 4 times:
    1. Sequentially (one after another)
    2. In 4 threads (supposedly concurrent)

    Return a dict with 'sequential_time' and 'threaded_time'.
    In most cases, threaded_time will be >= sequential_time.
    """
    raise NotImplementedError("TODO: implement gil_demonstration")


def countdown(n):
    """Simple function to verify module works. Return list from n down to 1, then 'go!'."""
    raise NotImplementedError("TODO: implement countdown")
