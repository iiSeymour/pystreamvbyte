import numpy as np
from time import perf_counter
from contextlib import contextmanager


def generate_data(rmax=256, size=int(1e5), dtype=np.uint32):
    return np.random.randint(0, rmax, size=size, dtype=dtype)


def convert_bytes(length, suffix="B"):
    """
    Return bytes in human readable format.

    >>> convert_bytes(10)
    '10 B'
    >>> convert_bytes(10001)
    '10.00 KB'
    >>> convert_bytes(23123456789)
    '23.12 GB'
    """
    return "%6.3f %s%s" % (length / 1e9, 'G', suffix)

    for idx, unit in enumerate(['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']):
        if abs(length) < 1000.0:
            if idx == 0:
                return "%6.0f %s%s" % (length, unit, suffix)
            else:
                return "%6.2f %s%s" % (length, unit, suffix)
        length /= 1000.0


@contextmanager
def time(name):
    t0 = perf_counter()
    yield
    t1 = perf_counter() - t0
    print("%s time %.6f s," % (name, t1))


@contextmanager
def benchmark(name, size, dtype):
    t0 = perf_counter()
    yield
    t1 = perf_counter() - t0
    print("%s time %.6f s," % (name, t1), end=" ")
    nbytes = np.dtype(dtype).itemsize
    print("{:15,} {}s/sec ({})".format(int(size / t1), dtype, convert_bytes(int(size * nbytes / t1), suffix="B/s")))
