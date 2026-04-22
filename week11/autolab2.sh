#!/bin/bash
#BSUB -J autolab2[2,29,71-73:2,127]
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 10
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -M 2GB
#BSUB -o autolab2_%J.out
#BSUB -e autolab2_%J.err

echo "hej"
