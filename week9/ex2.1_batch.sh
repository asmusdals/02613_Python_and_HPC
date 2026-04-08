#!/bin/bash
#
# Run with:
#   bsub < ex2.1_batch.sh
#
#BSUB -J week9_ex2_1_gpu
#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 00:10
#BSUB -o ex2_1_%J.out
#BSUB -e ex2_1_%J.err

set -euo pipefail

cd "${LS_SUBCWD:-$PWD}"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

python -u ex2.1.py
