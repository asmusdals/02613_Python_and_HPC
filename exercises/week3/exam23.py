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
tiled_array = np.tile(np.arange(256, dtype=np.uint8), (n // 256) * n * n).reshape(n, n, n) 

# save array to a file using write_numpy and write_blosc and print time for each function
start = time.time()
write_numpy(tiled_array, "numpy_array")
end = time.time()
print(f"Time taken to write numpy array: {end - start} seconds")    
start = time.time()
write_blosc(tiled_array, "blosc_array")
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

# n-62-30-5(s224473) $ python ex_2.3.py 256
# Time taken to write numpy array: 0.3362386226654053 seconds
# Time taken to write blosc array: 0.010513782501220703 seconds
# Time taken to read numpy array: 0.14774179458618164 seconds
# Time taken to read blosc array: 0.008727312088012695 seconds
# (02613_2026) ~/Documents/02613/old_setup/week3
# n-62-30-5(s224473) $ python ex_2.3.py 512
# Time taken to write numpy array: 1.5377492904663086 seconds
# Time taken to write blosc array: 0.07929587364196777 seconds
# Time taken to read numpy array: 1.1672801971435547 seconds
# Time taken to read blosc array: 0.05461287498474121 seconds
# (02613_2026) ~/Documents/02613/old_setup/week3
# n-62-30-5(s224473) $ python ex_2.3.py 1024
# Time taken to write numpy array: 9.994951963424683 seconds
# Time taken to write blosc array: 0.44855499267578125 seconds
# Time taken to read numpy array: 9.357367515563965 seconds
# Time taken to read blosc array: 0.41307592391967773 seconds
# (02613_2026) ~/Documents/02613/old_setup/week3
# n-62-30-5(s224473) $ 