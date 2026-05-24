#!/bin/bash
#BSUB -J autolab_2_3
#BSUB -q hpc
#BSUB -n 8
#BSUB -W 30
#BSUB -R "select[model==XeonGold6126]"
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -M 2GB
#BSUB -o /work3/02613/dump/autolab_2_3_%J.out
#BSUB -e /work3/02613/dump/autolab_2_3_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

NUM_THREADS=8
export OMP_NUM_THREADS=$NUM_THREADS
export MPI_NUM_THREADS=$NUM_THREADS
export MKL_NUM_THREADS=$NUM_THREADS
export OPENBLAS_NUM_THREADS=$NUM_THREADS

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_DIR"

python -u autolab_2_3.py
