#!/bin/bash

#BSUB -J dmi_parquet
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 10
#BSUB -R "select[model==XeonGold6126]"
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -M 4GB
#BSUB -o job_%J.out
#BSUB -e job_%J.err
#BSUB -u s224473@student.dtu.dk
#BSUB -B
#BSUB -N

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python -u ex3.py /dtu/projects/02613_2025/data/dmi/2023_01.csv.zip dmi_parquet_chunks