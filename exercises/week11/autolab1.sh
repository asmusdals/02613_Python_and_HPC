#!/bin/bash
#BSUB -J autolab1[1-10]
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 10
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -M 2GB
#BSUB -o job_%J.out
#BSUB -e job_%J.err

echo "hej"
