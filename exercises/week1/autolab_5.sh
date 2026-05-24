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


#eksamenslæsning: 
#!/bin/bash
#BSUB -J autolab5
#BSUB -q hpc
#BSUB -W 2
#BSUB -R "rusage[mem=512MB]"
#BSUB -n 16 #antallet af cores
#BSUB -R "span[hosts=1]"
#BSUB -o autolab4_%.out
#BSUB -e autolab4_%.err

lscpu
/bin/sleep 60