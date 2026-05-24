import sys
import numpy as np

diagonal = np.array([int(x) for x in sys.argv[1:]])
matrix = np.diag(diagonal)

print(matrix)
np.save("matrix.npy", matrix)
