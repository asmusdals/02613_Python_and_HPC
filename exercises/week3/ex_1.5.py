import numpy as np
import time

repetitions = 100  # mindst 100

# Logaritmisk fordelte SIZE fra 10^2 til 10^8
sizes = np.logspace(2, 8, num=10).astype(int)

for SIZE in sizes:
    mat = np.random.rand(1, SIZE).astype(np.float32)

    start_time = time.perf_counter()
    for _ in range(repetitions):
        double_row = 2 * mat[0, :]
    end_time = time.perf_counter()

    row_time = end_time - start_time
    print(f"SIZE={SIZE} | row: {row_time:.6f}s")
