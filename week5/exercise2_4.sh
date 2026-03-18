#!/bin/bash

#BSUB -J autolab_2_1                 # Jobnavn (vises i jobkøen)
#BSUB -q hpc                         # Queue der bruges på DTU HPC
#BSUB -n 24                          # Antal CPU-cores der reserveres
#BSUB -W 10                          # Maksimal køretid (walltime) i minutter
#BSUB -R "select[model==XeonGold6126]"  # Kør på specifik CPU-model for reproducérbare benchmarks
#BSUB -R "span[hosts=1]"             # Alle cores skal ligge på samme node
#BSUB -R "rusage[mem=2GB]"           # Reserver 2GB RAM pr core
#BSUB -M 2GB                         # Hard memory limit pr proces
#BSUB -o job_%J.out                  # Standard output fil (%J = job-id)
#BSUB -e job_%J.err                  # Error output fil
#BSUB -u s224473@student.dtu.dk      # Email til jobnotifikationer
#BSUB -B                             # Send email når jobbet starter
#BSUB -N                             # Send email når jobbet slutter

source /dtu/projects/02613_2025/conda/conda_init.sh   # Load conda environment
conda activate 02613                                  # Aktiver kursus-miljø



echo "Host: $(hostname)"
echo "Allocated cores (LSB_DJOB_NUMPROC): $LSB_DJOB_NUMPROC"
echo "Working dir: $(pwd)"

# --- Benchmark: run fastest implementation for p=1..24 ---
echo "p,real" > timings.csv

for p in $(seq 1 24); do
  # /usr/bin/time skriver til stderr; vi fanger kun real-sekunder (%e)
  t=$(/usr/bin/time -f "%e" python -u modified_chunk.py "$p" 2>&1 >/dev/null)
  echo "$p,$t" >> timings.csv
done

echo "Saved timings.csv:"
head -n 5 timings.csv
echo "..."
tail -n 5 timings.csv

# --- Plot speedup (expects plot_speedup.py in same folder) ---
python -u plot_speedup.py

echo "Done. Generated files:"
ls -lh timings.csv speedup.png 2>/dev/null || true