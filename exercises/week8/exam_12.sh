#!/bin/bash
#BSUB -J exam_12_chunks
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 10
#BSUB -R "select[model==XeonGold6126]"
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=4GB]"
#BSUB -M 4GB
#BSUB -o exam_12_%J.out
#BSUB -e exam_12_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

FILE=/dtu/projects/02613_2025/data/dmi/2023_01.csv.zip

lscpu

for CHUNK_SIZE in 1000 10000 100000 1000000
do
    echo "chunk_size=$CHUNK_SIZE"
    /usr/bin/time -f "mem=%M KB runtime=%e s" python -u exam_11.py "$FILE" "$CHUNK_SIZE" 2>&1
    echo
done




# chunk_size=1000
# 12548.630000000054
# mem=130980 KB runtime=28.78 s

# chunk_size=10000
# 12548.629999999994
# mem=134544 KB runtime=15.92 s

# chunk_size=100000
# 12548.629999999997
# mem=192296 KB runtime=15.06 s

# chunk_size=1000000
# 12548.630000000001
# mem=572252 KB runtime=15.32 s
