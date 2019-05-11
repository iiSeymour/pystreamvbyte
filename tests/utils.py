import numpy as np
from time import perf_counter
from contextlib import contextmanager


def generate_data(rmax=256, size=int(1e5), dtype=np.uint32):
    return np.random.randint(0, rmax, size=size, dtype=dtype)


@contextmanager
def time(name):
    t0 = perf_counter()
    yield
    t1 = perf_counter() - t0
    print("%s time %.6f s," % (name, t1))


@contextmanager
def benchmark(name, size):
    t0 = perf_counter()
    yield
    t1 = perf_counter() - t0
    print("%s time %.6f s," % (name, t1), end=" ")
    print("{:,} uints/sec".format(int(size / t1)))
