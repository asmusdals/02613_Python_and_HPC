#!/bin/bash
#BSUB -J haversine
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 10
#BSUB -R "select[model==XeonGold6126]"
#BSUB -R "span[hosts=1]"             
#BSUB -R "rusage[mem=2GB]"           
#BSUB -o haversine_%J.out
#BSUB -e haversine_%J.err
#BSUB -u s224473@student.dtu.dk
#BSUB -N

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python -u haversine.py /dtu/projects/02613_2025/data/locations/locations_100.csv


# /zhome/5d/2/186790/Documents/02613/old_setup/week4
# ~/Documents/02613/old_setup/week4
# n-62-9-42(s224473) $ ls /dtu/projects/02613_2025/data/locations/
# locations.csv      locations_1000.csv  locations_500.csv
# locations_100.csv  locations_2000.csv  locations_5000.csv

