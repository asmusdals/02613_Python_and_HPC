#!/bin/bash
#BSUB -J blosc_vs_numpy 
#BSUB -q hpc
#BSUB -W 2
#BSUB -R "select[model == XeonGold6126] rusage[mem=8GB]"
#BSUB -M 8GB
#BSUB -n 1
#BSUB -o blosc_vs_numpy_%J.out
#BSUB -e blosc_vs_numpy_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python -u autolab_2.1.py 256
python -u autolab_2.1.py 512
python -u autolab_2.1.py 1024