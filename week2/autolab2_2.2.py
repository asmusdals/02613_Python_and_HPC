import sys
import numpy as np

vector = np.array([int(x) for x in sys.argv[1:]])

def magnitude(vector):
    return np.sqrt(np.sum(vector**2))

print(magnitude(vector))