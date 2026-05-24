#!/bin/bash
#BSUB -J ex21[1-202]
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 20
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -M 2GB
#BSUB -o ex21_%J_%I.out
#BSUB -e ex21_%J_%I.err

set -eo pipefail

cd "${LS_SUBCWD:-$PWD}"

set +u
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613
set -u

python -u ex21.py "${LSB_JOBINDEX}"
