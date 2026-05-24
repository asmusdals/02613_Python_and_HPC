import time

import numpy as np
from numba import jit


def matmul(A, B):
    C = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for k in range(B.shape[1]):
            for j in range(A.shape[1]):
                C[i, j] += A[i, k] * B[k, j]
    return C


@jit(nopython=True)
def jit_matmul(A, B):
    C = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for k in range(B.shape[1]):
            for j in range(A.shape[1]):
                C[i, j] += A[i, k] * B[k, j]
    return C


A = np.random.rand(200, 200)
B = np.random.rand(200, 200)

start = time.time()
C = matmul(A, B)
end = time.time()
python_time = end - start

jit_matmul(A, B)

start = time.time()
D = jit_matmul(A, B)
end = time.time()
jit_time = end - start

print("Python time:", python_time)
print("JIT time:", jit_time)
print("Speedup:", python_time / jit_time)
print("Same result:", np.allclose(C, D))


# Python time: 0.6018109321594238
# JIT time: 0.0009911060333251953
# Speedup: 607.2114505653116
# Same result: True



# 1.3 answer
# Most cache-efficient loop order is (i, k, j)
# because NumPy arrays are stored row-wise (C-order).
# With j as the innermost loop, we access B[k, j] and C[i, j]
# sequentially along rows (contiguous memory), which is cache-friendly.
# Other orders (e.g. i, j, k) access B column-wise, causing cache misses
# and slower performance.


########################################################################

# 1.4 answer
# Python time: 6.369863033294678
# JIT time: 0.0021071434020996094
# Speedup: 3022.9850644942294

