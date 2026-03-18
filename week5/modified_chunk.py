import random
import multiprocessing
import sys

def sample():
    x = random.uniform(-1.0, 1.0)
    y = random.uniform(-1.0, 1.0)
    if x**2 + y**2 <= 1:
        return 1
    else:
        return 0

def sample_multiple(samples_partial):
    return sum(sample() for _ in range(samples_partial))

if __name__ == "__main__":
    
    samples = 1000000
    
    # n_proc tages fra command line argument
    n_proc = int(sys.argv[1])

    chunk_size = samples // n_proc

    pool = multiprocessing.Pool(n_proc)

    results_async = [
        pool.apply_async(sample_multiple, (chunk_size,))
        for _ in range(n_proc)
    ]

    hits = sum(r.get() for r in results_async)

    pi = 4.0 * hits / samples

    print(pi)