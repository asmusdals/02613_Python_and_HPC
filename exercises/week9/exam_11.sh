#!/bin/bash
#BSUB -J exam_11_numba
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 10
#BSUB -R "select[model==XeonGold6126]"
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -M 2GB
#BSUB -o exam_11_%J.out
#BSUB -e exam_11_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

lscpu
python -u exam_11.py 200
