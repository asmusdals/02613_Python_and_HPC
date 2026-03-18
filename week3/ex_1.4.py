import numpy as np
import matplotlib.pyplot as plt

# Indsæt dine målinger her manuelt (fra .out filen)
SIZE = np.array([10,24,59,146,359,879,2154,5274,12915])
col_time = np.array([0.002226,0.002216,0.001757,0.001747,
                     0.002095,0.002312,0.003118,0.005301,0.013869])
row_time = np.array([0.002186,0.002199,0.001570,0.001592,
                     0.001666,0.001816,0.001999,0.002439,0.003302])

repetitions = 1000

# FLOPs
flops = repetitions * SIZE

# MFLOP/s
col_mflops = flops / col_time / 1e6
row_mflops = flops / row_time / 1e6

# Matrix size in kB (float32 assumed)
matrix_kb = SIZE**2 * 4 / 1024

# -------- Plot performance --------
plt.figure()
plt.loglog(matrix_kb, col_mflops, 'o-', label="Column")
plt.loglog(matrix_kb, row_mflops, 'o-', label="Row")
plt.xlabel("Matrix size (kB)")
plt.ylabel("Performance (MFLOP/s)")
plt.legend()
plt.title("Row vs Column Performance")
plt.show()

# -------- Plot ratio --------
plt.figure()
plt.loglog(matrix_kb, col_mflops / row_mflops, 'o-')
plt.xlabel("Matrix size (kB)")
plt.ylabel("Column / Row MFLOP/s")
plt.title("Performance Ratio")
plt.show()
