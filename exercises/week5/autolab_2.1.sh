#!/bin/bash

#BSUB -J autolab_2_1                 # Jobnavn (vises i jobkøen)
#BSUB -q hpc                         # Queue der bruges på DTU HPC
#BSUB -n 10                          # Antal CPU-cores der reserveres
#BSUB -W 10                          # Maksimal køretid (walltime) i minutter
#BSUB -R "select[model==XeonGold6126]"  # Kør på specifik CPU-model for reproducérbare benchmarks
#BSUB -R "span[hosts=1]"             # Alle cores skal ligge på samme node
#BSUB -R "rusage[mem=2GB]"           # Reserver 2GB RAM pr core
#BSUB -M 2GB                         # Hard memory limit pr proces
#BSUB -o job_%J.out                  # Standard output fil (%J = job-id)
#BSUB -e job_%J.err                  # Error output fil
#BSUB -u s224473@student.dtu.dk      # Email til jobnotifikationer
#BSUB -B                             # Send email når jobbet starter
#BSUB -N                             # Send email når jobbet slutter

source /dtu/projects/02613_2025/conda/conda_init.sh   # Load conda environment
conda activate 02613                                  # Aktiver kursus-miljø

time python -u pi_serial.py
time python -u pi_fully_parallel.py
time python -u pi_chunked_parallel.py


# resultater: 
# Note on expected timings:
# The fully parallel version can be much slower than the serial version because it
# creates one multiprocessing task per sample. Each task does very little work, so
# most of the runtime is spent on overhead: scheduling tasks, communicating between
# processes, creating AsyncResult objects, and collecting results. This is visible
# as high sys time. The chunked version is faster because each process gets one
# large block of samples, so there are far fewer tasks and much less overhead.
# real	0m0.748s
# user	0m0.685s
# sys	0m0.016s

# real	1m34.258s
# user	2m21.686s
# sys	1m4.627s

# real	0m0.263s
# user	0m0.711s
# sys	0m0.083s
