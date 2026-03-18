#!/bin/bash
#BSUB -J notify
#BSUB -q hpc
#BSUB -W 2
#BSUB -B 
#BSUB -N
#BSUB -u s224473@dtu.dk
#BSUB -o notify_%J.out
#BSUB -e notify_%J.err

/bin/sleep 60
