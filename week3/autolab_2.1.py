import sys
import time
import numpy as np
import blosc
import os


def write_numpy(arr, file_name):
    np.save(f"{file_name}.npy", arr)
    os.sync()


def write_blosc(arr, file_name, cname="lz4"):
    b_arr = blosc.pack_array(arr, cname=cname)
    with open(f"{file_name}.bl", "wb") as w:
        w.write(b_arr)
    os.sync()


def read_numpy(file_name):
    return np.load(f"{file_name}.npy")


def read_blosc(file_name):
    with open(f"{file_name}.bl", "rb") as r:
        b_arr = r.read()
    return blosc.unpack_array(b_arr)


n = int(sys.argv[1])

# 3d array of zeroes of size n x n x n
arr = np.zeros((n, n, n), dtype=np.uint8)

# save array to a file using write_numpy and write_blosc and print time for each function
start = time.time()
write_numpy(arr, "numpy_array")
end = time.time()
print(f"Time taken to write numpy array: {end - start} seconds")    
start = time.time()
write_blosc(arr, "blosc_array")
end = time.time()
print(f"Time taken to write blosc array: {end - start} seconds")

# read array from created file using read_numpy and read_blosc
start = time.time()
read_numpy("numpy_array")
end = time.time()
print(f"Time taken to read numpy array: {end - start} seconds")    
start = time.time()
read_blosc("blosc_array")
end = time.time()
print(f"Time taken to read blosc array: {end - start} seconds")

