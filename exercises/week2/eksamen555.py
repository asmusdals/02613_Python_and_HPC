import numpy as np 
import sys
import time

path = sys.argv[1]
p = int(sys.argv[2])

A = np.load(path)

start = time.perf_counter()

B = A.copy()
for _ in range(p):
    B = B @ A

end = time.perf_counter()

np.save("multiple_matrix", B)

# B = np.array([[1,3],[5,7]])
# np.save("stock_matrix", B)
muldrengen = np.load("multiple_matrix.npy")
print(muldrengen)
print(f"time blev sgu {end-start}")
