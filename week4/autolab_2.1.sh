#!/bin/bash
#BSUB -J haversine
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 10
#BSUB -R "select[model==XeonGold6126]"
#BSUB -o haversine_%J.out
#BSUB -e haversine_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python -u haversine.py input.csv