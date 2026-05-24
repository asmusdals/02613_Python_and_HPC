# import numpy as np
# import time

# SIZE = 100

# n_repeat = int(1000)
# mat = np.random.rand(SIZE, SIZE)

# start1 = time.perf_counter()
# for _ in range(n_repeat): 
#     double_column = 2 * mat[:, 0]
# end1 = time.perf_counter()
# print((end1-start1)/n_repeat)

# start2 = time.perf_counter()
# for _ in range(n_repeat):
#     double_row = 2 * mat[0, :]
# end2 = time.perf_counter()
# print((end2-start2)/n_repeat)

from time import perf_counter as time

import numpy as np

SIZE = 100

n_repeat = int(1e3)
mat = np.random.rand(SIZE, SIZE)

trow = time()
for _ in range(n_repeat):
    mat[0, :] * 1.01
trow = time() - trow

tcol = time()
for _ in range(n_repeat):
    mat[:, 0] * 1.01
tcol = time() - tcol

print('trow =', trow / n_repeat)
print('tcol =', tcol / n_repeat)