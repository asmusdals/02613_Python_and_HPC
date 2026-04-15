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

    # Generate random float32 numbers
    x = np.random.rand(n).astype(np.float32)

    # Copy to GPU
    d_x = cuda.to_device(x)

    # Run reduction
    result = reduce(d_x)

    # Copy result back and print ONLY the sum
    print(result.copy_to_host()[0])


# (02613_2026) ~/Documents/02613/week10
# n-62-20-1(s224473) $ nsys stats ex4.nsys-rep 
# Generating SQLite file ex4.sqlite from ex4.nsys-rep
# Exporting 4366 events: [===================================================100%]
# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/nvtxsum.py]... 
# SKIPPED: ex4.sqlite does not contain NV Tools Extension (NVTX) data.

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/osrtsum.py]... 

#  ** OS Runtime Summary (osrtsum):

#  Time (%)  Total Time (ns)  Num Calls   Avg (ns)     Med (ns)    Min (ns)  Max (ns)   StdDev (ns)           Name         
#  --------  ---------------  ---------  -----------  -----------  --------  ---------  -----------  ----------------------
#      45.8        733680100          2  366840050.0  366840050.0   3700886  729979214  513556330.8  sem_wait              
#      39.6        634867547         21   30231788.0    2192858.0      2053  133310399   45182176.0  poll                  
#       7.1        114548903        648     176773.0     191252.5      2864     364389      64963.7  open64                
#       5.7         92084455        778     118360.5      17349.5      1022   32819725    1288635.6  ioctl                 
#       0.5          8225640        658      12501.0       3830.0      1000     201024      21624.3  read                  
#       0.4          6193561        615      10070.8       2300.0      1825    3639397     146924.8  mmap64                
#       0.3          4128644         45      91747.6       5263.0      2624    1009298     209999.9  fopen                 
#       0.2          3070535        536       5728.6       5473.5      3570      13585       1254.5  munmap                
#       0.2          2507200         31      80877.4       1073.0      1004     673088     211166.3  fcntl                 
#       0.1           817511          4     204377.8     167978.0     53910     427645     182127.3  pthread_create        
#       0.0           587786         11      53435.1       6001.0      3189     293064     106471.5  fread                 
#       0.0           410133          8      51266.6       5031.0      3824     208819      85428.0  fopen64               
#       0.0           406162         40      10154.1       6890.5      1397     114038      17899.9  fclose                
#       0.0           313582         14      22398.7      23191.5     13598      38820       6298.5  sem_timedwait         
#       0.0           286685         21      13651.7       8373.0      3815     100897      20515.4  mmap                  
#       0.0           127962          8      15995.3       9228.0      1129      73871      23795.7  fgets                 
#       0.0           113150          1     113150.0     113150.0    113150     113150          0.0  pthread_cond_wait     
#       0.0            75451         20       3772.6       3296.5      1158       8446       1580.9  write                 
#       0.0            29365          6       4894.2       5151.5      2292       7053       1661.4  open                  
#       0.0            22358          3       7452.7       8844.0      4166       9348       2857.5  pipe2                 
#       0.0            15652          2       7826.0       7826.0      5862       9790       2777.5  socket                
#       0.0             9078          1       9078.0       9078.0      9078       9078          0.0  connect               
#       0.0             7243          5       1448.6       1147.0      1040       2008        507.8  sigaction             
#       0.0             6752          2       3376.0       3376.0      3368       3384         11.3  pthread_cond_broadcast
#       0.0             4465          2       2232.5       2232.5      1519       2946       1009.0  fwrite                
#       0.0             2603          1       2603.0       2603.0      2603       2603          0.0  flockfile             
#       0.0             2292          2       1146.0       1146.0      1141       1151          7.1  dup                   
#       0.0             2286          1       2286.0       2286.0      2286       2286          0.0  mprotect              
#       0.0             1809          1       1809.0       1809.0      1809       1809          0.0  bind                  
#       0.0             1225          1       1225.0       1225.0      1225       1225          0.0  listen                

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/cudaapisum.py]... 

#  ** CUDA API Summary (cudaapisum):

#  Time (%)  Total Time (ns)  Num Calls  Avg (ns)   Med (ns)   Min (ns)  Max (ns)  StdDev (ns)           Name         
#  --------  ---------------  ---------  ---------  ---------  --------  --------  -----------  ----------------------
#      67.3          3576996          1  3576996.0  3576996.0   3576996   3576996          0.0  cuMemcpyHtoD_v2       
#       9.1           483355          2   241677.5   241677.5    137154    346201     147818.6  cuModuleLoadDataEx    
#       6.5           342855          2   171427.5   171427.5    162101    180754      13189.7  cuMemAlloc_v2         
#       5.8           309949          2   154974.5   154974.5    151162    158787       5391.7  cuLinkComplete        
#       3.0           161790          1   161790.0   161790.0    161790    161790          0.0  cuMemcpyDtoH_v2       
#       2.6           136591          2    68295.5    68295.5     68234     68357         87.0  cuLinkCreate_v2       
#       2.5           134496          9    14944.0    13245.0      8584     29180       7224.1  cuLaunchKernel        
#       1.7            91965        384      239.5      198.5       136      1794        128.2  cuGetProcAddress      
#       0.9            50239          1    50239.0    50239.0     50239     50239          0.0  cuMemGetInfo_v2       
#       0.4            19504          4     4876.0     4272.0      3755      7205       1576.4  cuStreamSynchronize   
#       0.1             3614          2     1807.0     1807.0      1428      2186        536.0  cuLinkDestroy         
#       0.1             3343          1     3343.0     3343.0      3343      3343          0.0  cuInit                
#       0.0              330          1      330.0      330.0       330       330          0.0  cuDeviceGetUuid_v2    
#       0.0              318          1      318.0      318.0       318       318          0.0  cuModuleGetLoadingMode

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/gpukernsum.py]... 

#  ** CUDA GPU Kernel Summary (gpukernsum):

#  Time (%)  Total Time (ns)  Instances  Avg (ns)  Med (ns)  Min (ns)  Max (ns)  StdDev (ns)      GridXYZ          BlockXYZ                                                     Name                                                
#  --------  ---------------  ---------  --------  --------  --------  --------  -----------  ----------------  --------------  ----------------------------------------------------------------------------------------------------
#      85.1           221150          1  221150.0  221150.0    221150    221150          0.0  125000    1    1    32    1    1  cudapy::__main__::reduce_kernel[abi:v1,cw51cXTLSUwv1sCUt9Uw11Ew0NRRQPKiLTj0gIGIFp_2b2oLQFEYYkHSQB1O…
#       4.7            12192          1   12192.0   12192.0     12192     12192          0.0  3907    1    1      32    1    1  cudapy::__main__::reduce_kernel[abi:v1,cw51cXTLSUwv1sCUt9Uw11Ew0NRRQPKiLTj0gIGIFp_2b2oLQFEYYkHSQB1O…
#       2.3             5920          2    2960.0    2960.0      2944      2976         22.6     1    1    1    1024    1    1  cudapy::numba::cuda::cudadrv::devicearray::_assign_kernel::_3clocals_3e::kernel[abi:v2,cw51cXTLSUwv…
#       1.8             4704          1    4704.0    4704.0      4704      4704          0.0   123    1    1    1024    1    1  cudapy::numba::cuda::cudadrv::devicearray::_assign_kernel::_3clocals_3e::kernel[abi:v2,cw51cXTLSUwv…
#       1.6             4192          1    4192.0    4192.0      4192      4192          0.0   123    1    1      32    1    1  cudapy::__main__::reduce_kernel[abi:v1,cw51cXTLSUwv1sCUt9Uw11Ew0NRRQPKiLTj0gIGIFp_2b2oLQFEYYkHSQB1O…
#       1.6             4129          1    4129.0    4129.0      4129      4129          0.0     4    1    1      32    1    1  cudapy::__main__::reduce_kernel[abi:v1,cw51cXTLSUwv1sCUt9Uw11Ew0NRRQPKiLTj0gIGIFp_2b2oLQFEYYkHSQB1O…
#       1.6             4128          1    4128.0    4128.0      4128      4128          0.0     1    1    1      32    1    1  cudapy::__main__::reduce_kernel[abi:v1,cw51cXTLSUwv1sCUt9Uw11Ew0NRRQPKiLTj0gIGIFp_2b2oLQFEYYkHSQB1O…
#       1.3             3424          1    3424.0    3424.0      3424      3424          0.0     4    1    1    1024    1    1  cudapy::numba::cuda::cudadrv::devicearray::_assign_kernel::_3clocals_3e::kernel[abi:v2,cw51cXTLSUwv…

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/gpumemtimesum.py]... 

#  ** GPU MemOps Summary (by Time) (gpumemtimesum):

#  Time (%)  Total Time (ns)  Count  Avg (ns)   Med (ns)   Min (ns)  Max (ns)  StdDev (ns)      Operation     
#  --------  ---------------  -----  ---------  ---------  --------  --------  -----------  ------------------
#      98.9          3372226      1  3372226.0  3372226.0   3372226   3372226          0.0  [CUDA memcpy HtoD]
#       1.1            39103      1    39103.0    39103.0     39103     39103          0.0  [CUDA memcpy DtoH]

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/gpumemsizesum.py]... 

#  ** GPU MemOps Summary (by Size) (gpumemsizesum):

#  Total (MB)  Count  Avg (MB)  Med (MB)  Min (MB)  Max (MB)  StdDev (MB)      Operation     
#  ----------  -----  --------  --------  --------  --------  -----------  ------------------
#      16.000      1    16.000    16.000    16.000    16.000        0.000  [CUDA memcpy HtoD]
#       0.500      1     0.500     0.500     0.500     0.500        0.000  [CUDA memcpy DtoH]

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/openmpevtsum.py]... 
# SKIPPED: ex4.sqlite does not contain OpenMP event data.

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/khrdebugsum.py]... 
# SKIPPED: ex4.sqlite does not contain KHR Extension (KHR_DEBUG) data.

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/khrdebuggpusum.py]... 
# SKIPPED: ex4.sqlite does not contain GPU KHR Extension (KHR_DEBUG) data.

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/vulkanmarkerssum.py]... 
# SKIPPED: ex4.sqlite does not contain Vulkan Debug Extension (Vulkan Debug Util) data.

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/vulkangpumarkersum.py]... 
# SKIPPED: ex4.sqlite does not contain GPU Vulkan Debug Extension (GPU Vulkan Debug markers) data.

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/dx11pixsum.py]... 
# SKIPPED: ex4.sqlite does not contain DX11 CPU debug markers.

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/dx12gpumarkersum.py]... 
# SKIPPED: ex4.sqlite does not contain DX12 GPU debug markers.

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/dx12pixsum.py]... 
# SKIPPED: ex4.sqlite does not contain DX12 CPU debug markers.

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/wddmqueuesdetails.py]... 
# SKIPPED: ex4.sqlite does not contain WDDM context data.

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/unifiedmemory.py]... 
# SKIPPED: ex4.sqlite does not contain CUDA Unified Memory CPU page faults data.

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/unifiedmemorytotals.py]... 
# SKIPPED: ex4.sqlite does not contain CUDA Unified Memory CPU page faults data.

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/umcpupagefaults.py]... 
# SKIPPED: ex4.sqlite does not contain CUDA Unified Memory CPU page faults data.

# Processing [ex4.sqlite] with [/appl/cuda/11.8.0/nsight-systems-2022.4.2/host-linux-x64/reports/openaccsum.py]... 
# SKIPPED: ex4.sqlite does not contain OpenACC event data.

# (02613_2026) ~/Documents/02613/week10
# n-62-20-1(s224473) $ 