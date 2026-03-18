#!/bin/bash
#BSUB -J notify
#BSUB -q hpc
#BSUB -W 2
#BSUB -R "select[model == XeonE5_2660v3]"
#BSUB -B
#BSUB -N
#BSUB -u s224473@dtu.dk
#BSUB -o notify_%J.out
#BSUB -e notify_%J.err

lscpu

/bin/sleep 60
