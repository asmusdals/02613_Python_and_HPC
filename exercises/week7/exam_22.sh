#!/bin/bash
#BSUB -J exam_22_arrow_pandas
#BSUB -q hpc
#BSUB -n 4
#BSUB -W 20
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -M 4GB
#BSUB -o exam_22_%J.out
#BSUB -e exam_22_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

lscpu
python -u exam_22.py /dtu/projects/02613_2025/data/dmi/2023_01.csv.zip



# === Exercise 2.2: PyArrow to pandas ===
# CSV path: /tmp/tmpwvhxq1gf/2023_01.csv
# Pandas read time:             11.461 s
# PyArrow read time:            3.037 s
# PyArrow to pandas time:       0.371 s
# PyArrow + conversion time:    3.408 s
# Speedup vs pure pandas:       3.36x
# Conclusion: PyArrow + conversion is faster than pure pandas.

# Pandas shape:                 (8142495, 7)
# PyArrow-converted shape:      (8142495, 7)
# PyArrow-converted memory:     919.13 MB

