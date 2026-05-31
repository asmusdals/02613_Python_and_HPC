import sys
import time

import numpy as np
from numba import jit


def matmul_python(a, b):
    c = np.zeros((a.shape[0], b.shape[1]))

    for i in range(a.shape[0]):
        for k in range(a.shape[1]):
            for j in range(b.shape[1]):
                c[i, j] += a[i, k] * b[k, j]

    return c


@jit(nopython=True)
def matmul_numba(a, b):
    c = np.zeros((a.shape[0], b.shape[1]))

    for i in range(a.shape[0]):
        for k in range(a.shape[1]):
            for j in range(b.shape[1]):
                c[i, j] += a[i, k] * b[k, j]

    return c


def time_function(function, a, b):
    start = time.perf_counter()
    result = function(a, b)
    elapsed = time.perf_counter() - start
    return result, elapsed


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200

    rng = np.random.default_rng(42)
    a = rng.random((n, n))
    b = rng.random((n, n))

    python_result, python_time = time_function(matmul_python, a, b)

    matmul_numba(a, b)
    numba_result, numba_time = time_function(matmul_numba, a, b)

    print(f"Python time: {python_time}")
    print(f"Numba time: {numba_time}")
    print(f"Speedup: {python_time / numba_time}")
    print(f"Same result: {np.allclose(python_result, numba_result)}")


if __name__ == "__main__":
    main()
