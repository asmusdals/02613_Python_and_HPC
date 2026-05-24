import ctypes
import multiprocessing as mp
import sys
from time import perf_counter as time
import numpy as np
from PIL import Image


def init(shared_arr_):
    global shared_arr
    shared_arr = shared_arr_


def tonumpyarray(mp_arr):
    return np.frombuffer(mp_arr, dtype='float32')


def reduce_step(args):
    b, offset, elemshape = args
    arr = tonumpyarray(shared_arr).reshape((-1,) + elemshape)

    # Add neighbor at distance "offset"
    # Example:
    # offset=1 -> arr[0]+=arr[1], arr[2]+=arr[3], ...
    # offset=2 -> arr[0]+=arr[2], arr[4]+=arr[6], ...
    # offset=4 -> arr[0]+=arr[4], ...
    arr[b] += arr[b + offset]


if __name__ == '__main__':
    n_processes = 1
    chunk = 2

    # Create shared array
    data = np.load(sys.argv[1]).astype('float32')
    n_images = len(data)
    elemshape = data.shape[1:]

    shared_arr = mp.RawArray(ctypes.c_float, data.size)
    arr = tonumpyarray(shared_arr).reshape(data.shape)
    np.copyto(arr, data)
    del data

    t = time()
    pool = mp.Pool(n_processes, initializer=init, initargs=(shared_arr,))

    # Full parallel reduction
    offset = 1
    while offset < n_images:
        tasks = [(i, offset, elemshape)
                 for i in range(0, n_images - offset, 2 * offset)]

        pool.map(reduce_step, tasks, chunksize=chunk)
        offset *= 2

    pool.close()
    pool.join()

    print(time() - t)

    # Mean image
    final_image = arr[0] / n_images

    Image.fromarray(
        (255 * final_image.astype(float)).astype('uint8')
    ).save('result.png')