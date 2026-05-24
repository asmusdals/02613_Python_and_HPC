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



#eksamenslæsning: 
#!/bin/bash
#BSUB -J autolab4
#BSUB -q hpc
#BSUB -W 2
#BSUB -R "rusage[mem=512MB]"
#BSUB -n 4 #antallet af cores
#BSUB -R "span[hosts=1]"
#BSUB -o autolab4_%.out
#BSUB -e autolab4_%.err

lscpu
/bin/sleep 60