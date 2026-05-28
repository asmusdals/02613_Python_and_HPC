#!/bin/bash
#BSUB -J exam_23_speedup
#BSUB -q hpc
#BSUB -n 24
#BSUB -W 30
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -M 2GB
#BSUB -o exam_23_%J.out
#BSUB -e exam_23_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

echo "CPU information from lscpu:"
lscpu
echo

MAX_THREADS=24
SAMPLES=1000000
REPEATS=3
CSV=exam_23_speedup.csv
PLOT=exam_23_speedup.png

echo "Running pi_chunked_parallel.py for n_proc from 1 to ${MAX_THREADS}"
echo "n_proc,time_seconds,speedup,pi" > "${CSV}"

T1=""
for N_PROC in $(seq 1 "${MAX_THREADS}"); do
    BEST_TIME=""
    BEST_PI=""

    for REPEAT in $(seq 1 "${REPEATS}"); do
        RESULT=$(python -u pi_chunked_parallel.py --samples "${SAMPLES}" --n-proc "${N_PROC}")
        TIME_SECONDS=$(echo "${RESULT}" | cut -d, -f2)
        PI_VALUE=$(echo "${RESULT}" | cut -d, -f3)

        if [ -z "${BEST_TIME}" ] || awk "BEGIN {exit !(${TIME_SECONDS} < ${BEST_TIME})}"; then
            BEST_TIME="${TIME_SECONDS}"
            BEST_PI="${PI_VALUE}"
        fi
    done

    if [ "${N_PROC}" -eq 1 ]; then
        T1="${BEST_TIME}"
    fi

    SPEEDUP=$(awk "BEGIN {printf \"%.6f\", ${T1} / ${BEST_TIME}}")
    echo "${N_PROC},${BEST_TIME},${SPEEDUP},${BEST_PI}" | tee -a "${CSV}"
done

python - <<'PY'
import csv

import matplotlib.pyplot as plt

csv_path = "exam_23_speedup.csv"
plot_path = "exam_23_speedup.png"

n_proc = []
speedup = []

with open(csv_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n_proc.append(int(row["n_proc"]))
        speedup.append(float(row["speedup"]))

plt.figure(figsize=(8, 5))
plt.plot(n_proc, speedup, marker="o", label="Measured speedup")
plt.plot(n_proc, n_proc, linestyle="--", color="gray", label="Ideal speedup")
plt.xlabel("Number of processes")
plt.ylabel("Speedup relative to n_proc=1")
plt.title("Speedup of pi_chunked_parallel.py")
plt.xticks(n_proc)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(plot_path, dpi=200)
PY

echo "Saved data to ${CSV}"
echo "Saved plot to ${PLOT}"
