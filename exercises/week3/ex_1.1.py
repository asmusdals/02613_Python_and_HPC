import numpy as np
import time

repetitions = 1000

# Logaritmisk fordelte SIZE fra 10^1 til 10^4.5
sizes = np.logspace(1, 4.5, num=10).astype(int)

for SIZE in sizes:
    mat = np.random.rand(SIZE, SIZE)

    # Column timing
    start_time = time.perf_counter()
    for _ in range(repetitions):
        double_column = 2 * mat[:, 0]
    end_time = time.perf_counter()
    column_time = end_time - start_time

    # Row timing
    start_time = time.perf_counter()
    for _ in range(repetitions):
        double_row = 2 * mat[0, :]
    end_time = time.perf_counter()
    row_time = end_time - start_time

    print(f"SIZE={SIZE} | column: {column_time:.6f}s | row: {row_time:.6f}s")
