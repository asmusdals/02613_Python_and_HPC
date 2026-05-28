#!/bin/bash
#BSUB -J mandelbrot
#BSUB -q hpc
#BSUB -n 4
#BSUB -W 10
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -M 2GB
#BSUB -o mandelbrot_%J.out
#BSUB -e mandelbrot_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

lscpu
python -u mandelbrot_parallel.py
