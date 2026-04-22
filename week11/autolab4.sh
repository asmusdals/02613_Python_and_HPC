#!/bin/bash
#BSUB -J autolab4[1-5]
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 10
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -M 2GB
#BSUB -w ended(array[*])
#BSUB -o autolab4_%J.out
#BSUB -e autolab4_%J.err
