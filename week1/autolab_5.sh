#!/bin/bash
#BSUB -J cores16
#BSUB -q hpc
#BSUB -W 2
#BSUB -n 16
#BSUB -R "span[hosts=1]"
#BSUB -o cores16_%J.out
#BSUB -e cores16_%J.err

lscpu
/bin/sleep 60
