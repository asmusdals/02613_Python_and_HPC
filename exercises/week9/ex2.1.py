import numpy as np
from numba import cuda


@cuda.jit
def add_kernel(x, y, out):
    i = cuda.grid(1)  # global tråd-indeks
    if i < x.size:    # undgå out-of-bounds
        out[i] = x[i] + y[i]


def main():
    if not cuda.is_available():
        raise RuntimeError(
            "CUDA is not available. Run this on a GPU node and activate the "
            "course environment (typically `02613_2026` for GPU code)."
        )

    n = 1_000_000
    x = np.random.rand(n).astype(np.float32)
    y = np.random.rand(n).astype(np.float32)

    d_x = cuda.to_device(x)
    d_y = cuda.to_device(y)
    d_out = cuda.device_array_like(x)

    threads_per_block = 256
    blocks_per_grid = (n + threads_per_block - 1) // threads_per_block

    # Warm-up so the kernel is JIT compiled before timing.
    add_kernel[blocks_per_grid, threads_per_block](d_x, d_y, d_out)
    cuda.synchronize()

    start = cuda.event(timing=True)
    end = cuda.event(timing=True)

    repeats = 20
    start.record()
    for _ in range(repeats):
        add_kernel[blocks_per_grid, threads_per_block](d_x, d_y, d_out)
    end.record()
    end.synchronize()

    ms_total = cuda.event_elapsed_time(start, end)
    ms_avg = ms_total / repeats

    out = d_out.copy_to_host()
    print("Kernel time avg (ms):", ms_avg)
    print("Correct:", np.allclose(out, x + y))


if __name__ == "__main__":
    main()
