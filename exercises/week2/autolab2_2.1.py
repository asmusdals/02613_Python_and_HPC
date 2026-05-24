# import numpy as np

# def magnitude(vector):
#     return np.sqrt(np.sum(vector**2))

# hej = np.array([1,1,3,3,4])
# print(magnitude(hej))







import numpy as np

def magnitude(arr):
    return np.sqrt(np.sum(arr**2)).astype(int)
a = np.array([1,1,3,3,4])
print(magnitude(a))