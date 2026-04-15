from numba import cuda
import sys
import numpy as np

TPB = 32  # Threads per block rettet fra 128 til 32 da autolab kun kører maks 64

@cuda.jit
def reduce_kernel(data, out, n):
    tid = cuda.threadIdx.x
    i = cuda.grid(1)

    # Shared memory for one block
    sdata = cuda.shared.array(shape=TPB, dtype=float32)

    # Load one element per thread into shared memory
    if i < n:
        sdata[tid] = data[i]
    else:
        sdata[tid] = 0.0

    cuda.syncthreads()

    # Reduction inside shared memory
    s = 1
    while s < cuda.blockDim.x:
        if tid % (2 * s) == 0 and tid + s < cuda.blockDim.x:
            sdata[tid] += sdata[tid + s]
        s *= 2
        cuda.syncthreads()

    # Write one result per block to global memory
    if tid == 0:
        out[cuda.blockIdx.x] = sdata[0]
        
def get_grid(n, tpb):
    return (n + (tpb - 1)) // tpb  # Blocks per grid

def reduce(x):
    n = len(x)
    bpg = get_grid(n, TPB)
    out = cuda.device_array(bpg, dtype=x.dtype)
    while bpg > 1:
        reduce_kernel[bpg, TPB](x, out, n)
        n = bpg
        bpg = get_grid(n, TPB)
        x[:n] = out[:n]
    reduce_kernel[bpg, TPB](x, out, n)
    return out

if __name__ == "__main__":
    n = int(sys.argv[1])

    # Generate random float32 numbers
    x = np.random.rand(n).astype(np.float32)

    # Copy to GPU
    d_x = cuda.to_device(x)

    # Run reduction
    result = reduce(d_x)

    # Copy result back and print ONLY the sum
    print(result.copy_to_host()[0])