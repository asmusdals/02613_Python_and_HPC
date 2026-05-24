#!/bin/bash
#BSUB -J autolab2
#BSUB -q hpc
#BSUB -W 2
#BSUB -o autolab2_%J.out
#BSUB -e autolab2_%J.err

/bin/sleep 60

#!/bin/bash
#BSUB -J autolab2
#BSUB -q hpc
#BSUB -W 2
#BSUB -o autolab2_%J.out
#BSUB -e autolab2_%J.err
#BSUB -u s224473@student.dtu.dk      # Email til jobnotifikationer
#BSUB -B                             # Send email når jobbet starter
#BSUB -N                             # Send email når jobbet slutter