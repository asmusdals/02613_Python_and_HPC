#!/bin/bash

#BSUB -J dmi_chunks
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

FILE=/dtu/projects/02613_2025/data/dmi/2023_01.csv.zip

echo "Benchmarking chunk sizes..."
echo

for CHUNK in 1000 10000 100000 1000000
do
    echo "Chunk size: $CHUNK"
    /usr/bin/time -f "mem=%M KB runtime=%e s" python -u autolab_1.py $FILE $CHUNK
    echo
done

# Ex2
# n-62-9-42(s224473) $ cat job_28102114.err 
# mem=130124 KB runtime=29.74 s
# mem=136740 KB runtime=17.28 s
# mem=197060 KB runtime=16.38 s
# mem=573944 KB runtime=16.95 s