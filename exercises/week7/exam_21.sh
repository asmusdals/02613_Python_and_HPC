#!/bin/bash
#BSUB -J exam_21_arrow
#BSUB -q hpc
#BSUB -n 4
#BSUB -W 20
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -M 4GB
#BSUB -o exam_21_%J.out
#BSUB -e exam_21_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

lscpu
python -u exam_21.py /dtu/projects/02613_2025/data/dmi/2023_01.csv.zip



# === Exercise 2.1: Reading DMI data with PyArrow ===
# CSV path: /tmp/tmptweejf8n/2023_01.csv
# Pandas read time:  14.204 s
# PyArrow read time: 3.466 s
# Speedup:           4.10x

# Pandas shape:      (8142495, 7)
# PyArrow rows:      8142495
# PyArrow columns:   7
# Pandas memory:     2045.10 MB
# PyArrow size:      507.57 MB

# PyArrow schema:
# coordsx: double
# coordsy: double
# created: timestamp[ns, tz=UTC]
# observed: timestamp[s, tz=UTC]
# parameterId: string
# stationId: int64
# value: double
