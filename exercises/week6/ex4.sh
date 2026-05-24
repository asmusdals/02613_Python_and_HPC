#!/bin/bash

#BSUB -J ex4
#BSUB -q hpc
#BSUB -n 10
#BSUB -W 30
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -M 2GB
#BSUB -o ex4_%J.out
#BSUB -e ex4_%J.err
#BSUB -u s224473@student.dtu.dk
#BSUB -B
#BSUB -N

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

DATA=/dtu/projects/02613_2025/data/celeba/celeba_100K.npy
CHUNK=32

for P in 1 2 4 8 10
do
    for RUN in 1 2 3
    do
        echo "processes=$P run=$RUN"
        python -u ex3.py $DATA $P $CHUNK
    done
done