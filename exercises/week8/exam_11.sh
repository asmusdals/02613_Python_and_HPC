#!/bin/bash
#BSUB -J exam_11_chunks
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 10
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -M 4GB
#BSUB -o exam_11_%J.out
#BSUB -e exam_11_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

lscpu
python -u exam_11.py /dtu/projects/02613_2025/data/dmi/2023_01.csv.zip 100000
