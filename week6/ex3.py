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
    arr[b] += arr[b + offset]


if __name__ == '__main__':
    n_processes = int(sys.argv[2])
    chunk = int(sys.argv[3])

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

    offset = 1
    while offset < n_images:
        tasks = [(i, offset, elemshape)
                 for i in range(0, n_images - offset, 2 * offset)]
        pool.map(reduce_step, tasks, chunksize=chunk)
        offset *= 2

    pool.close()
    pool.join()

    elapsed = time() - t
    print(elapsed)

    final_image = arr[0] / n_images
    Image.fromarray(
        (255 * final_image.astype(float)).astype('uint8')
    ).save('result.png')