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

# eksamenslæsning
#!/bin/bash 
#BSUB -J sleeper 
#BSUB -q hpc 
#BSUB -W 2
#BSUB -R ”rusage[mem=250GB]” 
#BSUB –n 8
#BSUB –R ”span[hosts=1]” 
#BSUB -o sleeper_%J.out 
#BSUB -e sleeper_%J.err
#BSUB -u s224473@student.dtu.dk      # Email til jobnotifikationer
#BSUB -B                             # Send email når jobbet starter
#BSUB -N                             # Send email når jobbet slutter

/bin/sleep 60