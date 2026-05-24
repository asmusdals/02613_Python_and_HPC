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

rand_array = np.random.randint(0,256,size=(n,)*3, dtype=np.uint8)
# save array to a file using write_numpy and write_blosc and print time for each function
start = time.time()
write_numpy(rand_array, "numpy_array")
end = time.time()
print(f"Time taken to write numpy array: {end - start} seconds")    
start = time.time()
write_blosc(rand_array, "blosc_array")
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

# (02613_2026) ~/Documents/02613/old_setup/week3
# n-62-30-5(s224473) $ python ex_2.4.py 256
# Time taken to write numpy array: 0.6574039459228516 seconds
# Time taken to write blosc array: 0.23388123512268066 seconds
# Time taken to read numpy array: 0.14770221710205078 seconds
# Time taken to read blosc array: 0.15505528450012207 seconds
# (02613_2026) ~/Documents/02613/old_setup/week3
# n-62-30-5(s224473) $ python ex_2.4.py 512
# Time taken to write numpy array: 1.3699071407318115 seconds
# Time taken to write blosc array: 1.3173136711120605 seconds
# Time taken to read numpy array: 1.1682047843933105 seconds
# Time taken to read blosc array: 1.2195024490356445 seconds
# (02613_2026) ~/Documents/02613/old_setup/week3
# n-62-30-5(s224473) $ python ex_2.4.py 1024
# Time taken to write numpy array: 10.407416343688965 seconds
# Time taken to write blosc array: 14.366328001022339 seconds
# Time taken to read numpy array: 9.317583084106445 seconds
# Time taken to read blosc array: 9.73929738998413 seconds
# (02613_2026) ~/Documents/02613/old_setup/week3
# n-62-30-5(s224473) $ 