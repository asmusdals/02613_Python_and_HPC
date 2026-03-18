#!/bin/bash
#BSUB -J cores64
#BSUB -q hpc
#BSUB -W 2
#BSUB -n 64
#BSUB -R "span[hosts=1]"
#BSUB -o cores64_%J.out
#BSUB -e cores64_%J.err

lscpu
/bin/sleep 60
