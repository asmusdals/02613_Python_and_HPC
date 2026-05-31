#!/bin/bash
#BSUB -J exam_31_parquet
#BSUB -q hpc
#BSUB -n 4
#BSUB -W 30
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -M 4GB
#BSUB -o exam_31_%J.out
#BSUB -e exam_31_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

lscpu
python -u exam_31.py /dtu/projects/02613_2025/data/dmi/2023_01.csv.zip



# === Exercise 3.1: CSV to Parquet ===
# CSV path:      /tmp/tmptlbgci95/2023_01.csv
# Parquet path:  2023_01.parquet
# CSV size:      694.72 MB
# Parquet size:  102.66 MB
# Size ratio:    CSV is 6.77x larger than Parquet
# Reduction:     85.2% smaller than CSV

# === Exercise 3.2: Read/write timing ===
# Read original CSV:       13.948 s
# Write CSV copy:          35.958 s
# Read CSV copy:           15.856 s
# Write Parquet:           4.170 s
# Read Parquet:            4.273 s

# Read speedup:            3.71x for Parquet compared with CSV
# Write speedup:           8.62x for Parquet compared with CSV