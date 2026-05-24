#!/bin/bash
#BSUB -J 1000rowreps
#BSUB -q hpc
#BSUB -W 2
#BSUB -R "select[model == XeonGold6126] rusage[mem=4GB]"
#BSUB -M 8GB
#BSUB -n 1
#BSUB -B
#BSUB -N
#BSUB -u s224473@dtu.dk
#BSUB -o 1000rowreps_%J.out
#BSUB -e 1000rowreps_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python -u ex_1.1.py
