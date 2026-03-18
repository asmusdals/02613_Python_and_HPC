#!/bin/bash
#BSUB -J cores
#BSUB -q hpc
#BSUB -W 2
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -o cores_%J.out
#BSUB -e cores_%J.err

lscpu
/bin/sleep 60
