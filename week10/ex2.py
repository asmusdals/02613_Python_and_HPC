from numba import cuda
import sys
import numpy as np

TPB = 32  # Threads per block rettet fra 128 til 32 da autolab kun kører maks 64

@cuda.jit
def reduce_kernel(data, out, n):
    # Get the 1D grid and block indices
    tid = cuda.threadIdx.x
    i = cuda.grid(1)

    # Do reduction for threadblock
    s = 1
    while s < cuda.blockDim.x:
        if tid % (2 * s) == 0 and i + s < n:
            data[i] += data[i + s]
        s *= 2
        cuda.syncthreads()  # Ensure block is synchronized

    # Write result for this block to global memory
    if tid == 0:
        out[cuda.blockIdx.x] = data[i]

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
    x = np.random.rand(n).astype(np.float32)
    result = reduce(x)
    print(result.copy_to_host()[0])


# når vi kører nsys profile -o glans python ex2.py 4000000 får vi filen 


# n-62-20-1(s224473) $ nsys stats glans.nsys-rep 
# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/nvtxsum.py]... 
# SKIPPED: glans.sqlite does not contain NV Tools Extension (NVTX) data.

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/osrtsum.py]... 

#  ** OS Runtime Summary (osrtsum):

#  Time (%)  Total Time (ns)  Num Calls   Avg (ns)     Med (ns)    Min (ns)  Max (ns)   StdDev (ns)           Name         
#  --------  ---------------  ---------  -----------  -----------  --------  ---------  -----------  ----------------------
#      44.7        615954559          2  307977279.5  307977279.5   2468291  613486268  432054955.0  sem_wait              
#      38.9        536559505         20   26827975.3    2076474.0      2183  134741644   44409079.9  poll                  
#       8.4        115338400        646     178542.4     192590.5      2728     429110      66290.9  open64                
#       6.1         84540428        794     106474.1      17049.5      1020   34167829    1236186.5  ioctl                 
#       0.8         10826511        704      15378.6       4491.0      1002     455288      32562.3  read                  
#       0.4          6166993        614      10044.0       2285.5      1815    3671083     148320.1  mmap64                
#       0.2          3014391        538       5603.0       5353.0      3519      12141       1185.0  munmap                
#       0.2          2774235         43      64517.1       6639.0      2988     747535     161729.6  fopen                 
#       0.1          1277514         26      49135.2       1073.5      1003     699637     170744.1  fcntl                 
#       0.1           829697          4     207424.3     180056.0     48822     420763     180362.8  pthread_create        
#       0.0           414243          7      59177.6       4962.0      2489     352383     129834.3  fread                 
#       0.0           403871         38      10628.2       8748.0      1523     110811      17700.2  fclose                
#       0.0           386554          8      48319.3       4726.0      3792     183322      79810.1  fopen64               
#       0.0           310437         23      13497.3       8896.0      3232     102560      19960.3  mmap                  
#       0.0           270988         14      19356.3      18844.0      9705      44530       8845.5  sem_timedwait         
#       0.0           133807          8      16725.9       9295.0      1086      75656      24335.4  fgets                 
#       0.0            80912          1      80912.0      80912.0     80912      80912          0.0  pthread_cond_wait     
#       0.0            67870         21       3231.9       2518.0      1020       8074       1853.9  write                 
#       0.0            31660          6       5276.7       5927.5      2346       7262       1893.8  open                  
#       0.0            24641          3       8213.7       9764.0      4088      10789       3609.5  pipe2                 
#       0.0            22479          1      22479.0      22479.0     22479      22479          0.0  pthread_cond_signal   
#       0.0            16496          2       8248.0       8248.0      6443      10053       2552.7  socket                
#       0.0            12472          4       3118.0       2503.0      1094       6372       2275.9  sigaction             
#       0.0            10713          1      10713.0      10713.0     10713      10713          0.0  connect               
#       0.0             5685          2       2842.5       2842.5      2839       2846          4.9  pthread_cond_broadcast
#       0.0             5635          2       2817.5       2817.5      2721       2914        136.5  flockfile             
#       0.0             5183          2       2591.5       2591.5      1852       3331       1045.8  fwrite                
#       0.0             2132          1       2132.0       2132.0      2132       2132          0.0  mprotect              
#       0.0             1894          1       1894.0       1894.0      1894       1894          0.0  bind                  
#       0.0             1452          1       1452.0       1452.0      1452       1452          0.0  listen                

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/cudaapisum.py]... 

#  ** CUDA API Summary (cudaapisum):

#  Time (%)  Total Time (ns)  Num Calls  Avg (ns)   Med (ns)   Min (ns)  Max (ns)  StdDev (ns)           Name         
#  --------  ---------------  ---------  ---------  ---------  --------  --------  -----------  ----------------------
#      53.8         17611977          5  3522395.4  3513357.0   3490023   3576584      32375.8  cuMemcpyHtoD_v2       
#      40.4         13223106         10  1322310.6  1266062.5     21000   2947353    1320132.8  cuMemcpyDtoH_v2       
#       3.2          1062185          6   177030.8   183627.0    156022    190332      15652.9  cuMemAlloc_v2         
#       1.0           335427          1   335427.0   335427.0    335427    335427          0.0  cuModuleLoadDataEx    
#       0.5           174674          1   174674.0   174674.0    174674    174674          0.0  cuLinkComplete        
#       0.4           126111          5    25222.2    24094.0     21918     30811       3484.0  cuLaunchKernel        
#       0.3            98133        384      255.6      200.5       139      2104        152.9  cuGetProcAddress      
#       0.2            72125          1    72125.0    72125.0     72125     72125          0.0  cuLinkCreate_v2       
#       0.2            54408          1    54408.0    54408.0     54408     54408          0.0  cuMemGetInfo_v2       
#       0.0             3237          1     3237.0     3237.0      3237      3237          0.0  cuInit                
#       0.0             1928          1     1928.0     1928.0      1928      1928          0.0  cuLinkDestroy         
#       0.0              332          1      332.0      332.0       332       332          0.0  cuDeviceGetUuid_v2    
#       0.0              264          1      264.0      264.0       264       264          0.0  cuModuleGetLoadingMode

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/gpukernsum.py]... 

#  ** CUDA GPU Kernel Summary (gpukernsum):

#  Time (%)  Total Time (ns)  Instances  Avg (ns)  Med (ns)  Min (ns)  Max (ns)  StdDev (ns)      GridXYZ          BlockXYZ                                                     Name                                                
#  --------  ---------------  ---------  --------  --------  --------  --------  -----------  ----------------  --------------  ----------------------------------------------------------------------------------------------------
#      89.4           222397          1  222397.0  222397.0    222397    222397          0.0  125000    1    1    32    1    1  cudapy::__main__::reduce_kernel[abi:v1,cw51cXTLSUwv1sCUt9Uw11Ew0NRRQPKiLTj0gIGIFp_2b2oLQFEYYkHSQB1O…
#       4.9            12095          1   12095.0   12095.0     12095     12095          0.0  3907    1    1      32    1    1  cudapy::__main__::reduce_kernel[abi:v1,cw51cXTLSUwv1sCUt9Uw11Ew0NRRQPKiLTj0gIGIFp_2b2oLQFEYYkHSQB1O…
#       2.0             4863          1    4863.0    4863.0      4863      4863          0.0   123    1    1      32    1    1  cudapy::__main__::reduce_kernel[abi:v1,cw51cXTLSUwv1sCUt9Uw11Ew0NRRQPKiLTj0gIGIFp_2b2oLQFEYYkHSQB1O…
#       1.9             4736          1    4736.0    4736.0      4736      4736          0.0     1    1    1      32    1    1  cudapy::__main__::reduce_kernel[abi:v1,cw51cXTLSUwv1sCUt9Uw11Ew0NRRQPKiLTj0gIGIFp_2b2oLQFEYYkHSQB1O…
#       1.9             4736          1    4736.0    4736.0      4736      4736          0.0     4    1    1      32    1    1  cudapy::__main__::reduce_kernel[abi:v1,cw51cXTLSUwv1sCUt9Uw11Ew0NRRQPKiLTj0gIGIFp_2b2oLQFEYYkHSQB1O…

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/gpumemtimesum.py]... 

#  ** GPU MemOps Summary (by Time) (gpumemtimesum):

#  Time (%)  Total Time (ns)  Count  Avg (ns)   Med (ns)   Min (ns)  Max (ns)  StdDev (ns)      Operation     
#  --------  ---------------  -----  ---------  ---------  --------  --------  -----------  ------------------
#      58.5         16621730      5  3324346.0  3318368.0   3301441   3366368      24582.3  [CUDA memcpy HtoD]
#      41.5         11795313     10  1179531.3  1110182.0      1823   2626504    1230867.2  [CUDA memcpy DtoH]

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/gpumemsizesum.py]... 

#  ** GPU MemOps Summary (by Size) (gpumemsizesum):

#  Total (MB)  Count  Avg (MB)  Med (MB)  Min (MB)  Max (MB)  StdDev (MB)      Operation     
#  ----------  -----  --------  --------  --------  --------  -----------  ------------------
#      81.016     10     8.102     8.250     0.000    16.000        8.328  [CUDA memcpy DtoH]
#      80.000      5    16.000    16.000    16.000    16.000        0.000  [CUDA memcpy HtoD]

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/openmpevtsum.py]... 
# SKIPPED: glans.sqlite does not contain OpenMP event data.

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/khrdebugsum.py]... 
# SKIPPED: glans.sqlite does not contain KHR Extension (KHR_DEBUG) data.

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/khrdebuggpusum.py]... 
# SKIPPED: glans.sqlite does not contain GPU KHR Extension (KHR_DEBUG) data.

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/vulkanmarkerssum.py]... 
# SKIPPED: glans.sqlite does not contain Vulkan Debug Extension (Vulkan Debug Util) data.

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/vulkangpumarkersum.py]... 
# SKIPPED: glans.sqlite does not contain GPU Vulkan Debug Extension (GPU Vulkan Debug markers) data.

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/dx11pixsum.py]... 
# SKIPPED: glans.sqlite does not contain DX11 CPU debug markers.

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/dx12gpumarkersum.py]... 
# SKIPPED: glans.sqlite does not contain DX12 GPU debug markers.

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/dx12pixsum.py]... 
# SKIPPED: glans.sqlite does not contain DX12 CPU debug markers.

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/wddmqueuesdetails.py]... 
# SKIPPED: glans.sqlite does not contain WDDM context data.

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/unifiedmemory.py]... 
# SKIPPED: glans.sqlite does not contain CUDA Unified Memory CPU page faults data.

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/unifiedmemorytotals.py]... 
# SKIPPED: glans.sqlite does not contain CUDA Unified Memory CPU page faults data.

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/umcpupagefaults.py]... 
# SKIPPED: glans.sqlite does not contain CUDA Unified Memory CPU page faults data.

# Processing [glans.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/openaccsum.py]... 
# SKIPPED: glans.sqlite does not contain OpenACC event data.

# (02613_2026) ~/Documents/02613/week10
# n-62-20-1(s224473) $ 



# SVAR PÅ OPGAVEN 
# 1. CUDA API Summary
# CUDA API Summary (cudaapisum)

# 👉 Den viser:

# hvad programmet bruger tid på fra CPU’ens perspektiv

# Her ser vi:

# cuMemcpyHtoD_v2 → 53.8%
# cuMemcpyDtoH_v2 → 40.4%
# cuLaunchKernel → ~0.4%

# 💡 Det betyder:

# næsten al tid går til kopiering af data
# meget lidt tid går til selve kernel-kørslen


# 2. GPU MemOps Summary (by Time)
# GPU MemOps Summary (by Time)

# 👉 Den bekræfter det samme:

# 58.5% → Host → Device
# 41.5% → Device → Host

# 💡 Altså:

# næsten 100% af GPU-tiden bruges på memory copies

# 🔹 Hvorfor ikke de andre tabeller?
# ❌ OS Runtime Summary
# viser CPU-systemkald (poll, sem_wait)
# ikke relevant for GPU-performance
# ❌ GPU Kernel Summary
# viser kun kernel execution
# ja, den er hurtig (~222 µs)
# men den siger ikke hvor total tid går hen

# 👉 den er god til:

# at se kernel performance
# 👉 men ikke til:
# at svare på “where is time spent?” (hele programmet)
# 🔥 Den rigtige måde at tænke på

# Spørgsmålet er:

# Where is time spent?

# 👉 Derfor skal du:

# kigge på hele pipeline
# ikke kun kernel
# 🔹 Perfekt eksamenssvar

# I look at the CUDA API Summary and GPU MemOps Summary, because they show 
# where time is spent in terms of GPU operations. These clearly show that 
# most of the runtime is dominated by memory transfers (host-to-device 
# and device-to-host), while kernel execution takes only a very small
# fraction of the total time.