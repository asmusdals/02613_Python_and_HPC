#!/bin/bash
#BSUB -J haversine_prof
#BSUB -q hpc
#BSUB -n 1
#BSUB -W 10
#BSUB -R "select[model==XeonGold6126]"
#BSUB -o haversine_prof_%J.out
#BSUB -e haversine_prof_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

# Kør med cProfile og gem stats
python -m cProfile -o profile_%J.prof haversine.py input.csv

# Print et kort, sorteret resume (top tid)
python - <<'PY'
import pstats, glob
fname = sorted(glob.glob("profile_*.prof"))[-1]
p = pstats.Stats(fname).strip_dirs().sort_stats("tottime")
p.print_stats(30)          # top 30 efter tottime
print("\n--- fokus på din fil (haversine.py) ---\n")
p.print_stats("haversine.py")
PY