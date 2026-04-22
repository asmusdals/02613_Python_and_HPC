#!/bin/bash
#BSUB -J autolab3[2,29,71-73:2,127]
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 10
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -M 2GB
#BSUB -w 1234567
#BSUB -o autolab3_%J.out
#BSUB -e autolab3_%J.err

echo "hej"
