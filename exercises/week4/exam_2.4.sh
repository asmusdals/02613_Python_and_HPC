#!/bin/bash
#BSUB -J exam_24
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 10
#BSUB -R "select[model==XeonGold6126]"
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -o exam_24_%J.out
#BSUB -e exam_24_%J.err
#BSUB -u s224473@student.dtu.dk
#BSUB -N

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

# Kør med cProfile og gem stats
python -m cProfile -o profile_%J.prof exam_2.3.py /dtu/projects/02613_2025/data/locations/locations_100.csv

# Print et kort, sorteret resume (top tid)
python - <<'PY'
import pstats, glob
fname = sorted(glob.glob("profile_*.prof"))[-1]
p = pstats.Stats(fname).strip_dirs().sort_stats("tottime")
p.print_stats(30)          # top 30 efter tottime
print("\n--- fokus på din fil (exam_2.3.py) ---\n")
p.print_stats("exam_2.3.py")
PY