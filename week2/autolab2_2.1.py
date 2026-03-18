import numpy as np

def magnitude(vector):
    return np.sqrt(np.sum(vector**2))

hej = np.array([1,1,3,3,4])
print(magnitude(hej))