import random
import multiprocessing
import argparse
import time

def sample():
    x = random.uniform(-1.0, 1.0)
    y = random.uniform(-1.0, 1.0)
    if x**2 + y**2 <= 1:
        return 1
    else:
        return 0

def sample_multiple(samples_partial):
    return sum(sample() for i in range(samples_partial))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=1000000)
    parser.add_argument("--n-proc", type=int, default=10)
    args = parser.parse_args()

    samples = args.samples
    n_proc = args.n_proc
    chunk_size = samples // n_proc
    chunks = [chunk_size] * n_proc
    chunks[-1] += samples % n_proc

    start = time.perf_counter()
    pool = multiprocessing.Pool(n_proc)
    results_async = [pool.apply_async(sample_multiple, (chunk,))
                    for chunk in chunks]
    hits = sum(r.get() for r in results_async)
    pool.close()
    pool.join()
    elapsed = time.perf_counter() - start

    pi = 4.0 * hits/samples
    print(f"{n_proc},{elapsed:.6f},{pi:.8f}")
