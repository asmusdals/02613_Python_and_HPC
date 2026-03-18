import numpy as np
import matplotlib.pyplot as plt

# ----- Indsæt dine målinger her -----
SIZE = np.array([
    100,
    464,
    2154,
    10000,
    46415,
    215443,
    1000000,
    4641588,
    21544346,
    100000000
])

row_time = np.array([
    0.000503,
    0.000506,
    0.000596,
    0.000890,
    0.002743,
    0.009931,
    0.059598,
    0.329822,
    2.758188,
    12.225744
])

repetitions = 100

# ----- Compute MFLOP/s -----
mflops = (repetitions * SIZE) / row_time / 1e6

# ----- Convert row size to kB (float32 = 4 bytes per element) -----
size_kb = SIZE * 4 / 1024

# ----- Cache sizes (Xeon Gold typical values) -----
L1_kb = 32
L2_kb = 1024
L3_kb = 19712  # ~19 MB

# ----- Plot -----
plt.figure()
plt.loglog(size_kb, mflops, 'o-', label="Row Doubling")

plt.axvline(L1_kb, linestyle='--', label="L1 (32 kB)")
plt.axvline(L2_kb, linestyle='--', label="L2 (1 MB)")
plt.axvline(L3_kb, linestyle='--', label="L3 (~19 MB)")

plt.xlabel("Row vector size (kB)")
plt.ylabel("Performance (MFLOP/s)")
plt.title("Row Doubling Performance vs Data Size")
plt.legend()
plt.grid(True, which="both")
plt.tight_layout()
plt.show()
