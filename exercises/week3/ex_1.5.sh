#!/bin/bash
#BSUB -J ex1.5 
#BSUB -q hpc
#BSUB -W 2
#BSUB -R "select[model == XeonGold6126] rusage[mem=8GB]"
#BSUB -M 8GB
#BSUB -n 1
#BSUB -o ex1.5_%J.out
#BSUB -e ex1.5_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python -u ex_1.5.py
