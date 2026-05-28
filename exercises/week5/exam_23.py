import argparse
import os
import subprocess
import tempfile
import time
from multiprocessing import Pool

from exercises.week5.pi_chunked_parallel_23 import sample_multiple


def max_threads_from_lscpu():
    try:
        output = subprocess.check_output(["lscpu"], text=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    for line in output.splitlines():
        if line.startswith("CPU(s):"):
            return int(line.split(":", 1)[1].strip())
    return None


def available_threads():
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0))
    return max_threads_from_lscpu() or os.cpu_count() or 1


def estimate_pi(samples, n_proc):
    chunk_size = samples // n_proc
    chunks = [chunk_size] * n_proc
    chunks[-1] += samples % n_proc

    with Pool(n_proc) as pool:
        hits = sum(pool.map(sample_multiple, chunks))

    return 4.0 * hits / samples


def time_run(samples, n_proc, repeats):
    times = []
    pi_values = []

    for _ in range(repeats):
        start = time.perf_counter()
        pi = estimate_pi(samples, n_proc)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        pi_values.append(pi)

    best_idx = min(range(len(times)), key=times.__getitem__)
    return times[best_idx], pi_values[best_idx]


def write_results(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write("n_proc,time_seconds,speedup,pi\n")
        for n_proc, elapsed, speedup, pi in rows:
            f.write(f"{n_proc},{elapsed:.6f},{speedup:.6f},{pi:.8f}\n")


def plot_speedup(path, rows):
    mpl_cache = os.path.join(tempfile.gettempdir(), "matplotlib_cache")
    os.makedirs(mpl_cache, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", mpl_cache)
    import matplotlib.pyplot as plt

    n_proc = [row[0] for row in rows]
    speedups = [row[2] for row in rows]

    plt.figure(figsize=(8, 5))
    plt.plot(n_proc, speedups, marker="o", label="Measured speedup")
    plt.plot(n_proc, n_proc, linestyle="--", color="gray", label="Ideal speedup")
    plt.xlabel("Number of processes")
    plt.ylabel("Speedup relative to n_proc=1")
    plt.title("Speedup of pi_chunked_parallel.py")
    plt.xticks(n_proc)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=200)


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark pi_chunked_parallel.py for n_proc from 1 to max threads."
    )
    parser.add_argument("--samples", type=int, default=1_000_000)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--max-proc", type=int, default=available_threads())
    parser.add_argument("--csv", default="exam_23_speedup.csv")
    parser.add_argument("--plot", default="exam_23_speedup.png")
    args = parser.parse_args()

    print(f"samples = {args.samples}")
    print(f"repeats = {args.repeats}")
    print(f"max processes = {args.max_proc}")

    rows = []
    t1 = None

    for n_proc in range(1, args.max_proc + 1):
        elapsed, pi = time_run(args.samples, n_proc, args.repeats)
        if n_proc == 1:
            t1 = elapsed
        speedup = t1 / elapsed
        rows.append((n_proc, elapsed, speedup, pi))
        print(
            f"n_proc={n_proc:2d}, time={elapsed:8.4f} s, "
            f"speedup={speedup:6.3f}, pi={pi:.6f}",
            flush=True,
        )

    write_results(args.csv, rows)
    plot_speedup(args.plot, rows)

    print(f"Saved data to {args.csv}")
    print(f"Saved plot to {args.plot}")


if __name__ == "__main__":
    main()
