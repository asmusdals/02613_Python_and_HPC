import numpy as np
import sys

path = sys.argv[1]

A = np.load(path)

np.save("cols.npy", A.mean(axis=0)) 
np.save("rows.npy", A.mean(axis=1))

x = np.load("cols.npy")
print(x)
print(x.shape)
print(x.dtype)

y = np.load("rows.npy")
print(y)
print(y.shape)
print(y.dtype)