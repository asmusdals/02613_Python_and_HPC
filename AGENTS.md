# 02613 Python and HPC Workflow

This repository is organized by week folders such as `week1/`, `week2/`, ..., `week8/`. New assignments should normally be placed in `weekN/` using the same flat structure already used in the repo. For a new week, create `week9/`, `week10/`, etc. and place scripts, notebooks, shell files, and notes directly in that folder unless the assignment clearly needs a deeper structure.

## First-pass repo workflow

When working in this repo:

1. Start by locating the relevant `weekN/` folder.
2. Keep new files inside that week folder unless they are shared repo-level context.
3. Reuse naming patterns already present in the repo, for example `autolab_*.py`, `autolab_*.sh`, `ex*.py`, and `ex*.sh`.
4. Use `context_folder/` as background reference material, not as the primary working area.

## DTU HPC workflow

The normal workflow is:

1. Develop or edit code locally in the relevant `weekN/` folder.
2. Transfer files to DTU HPC.
3. Log in to DTU HPC and activate the course conda environment.
4. Run quick tests interactively if needed.
5. Submit larger jobs with `bsub < script.sh`.
6. Inspect `.out` and `.err` files, adjust code or resources, and resubmit if needed.

## Conda environment rules

Before using the course environment on DTU HPC, run:

```bash
source /dtu/projects/02613_2025/conda/conda_init.sh
```

Then activate one of these environments:

```bash
conda activate 02613
```

Use `02613` for previous exercises and non-GPU work unless the assignment says otherwise.

```bash
conda activate 02613_2026
```

Use `02613_2026` for GPU code and the mini-project. The course announcement says GPU-topic code will only work in the new environment.

Important:

- If you change node, initialize conda again.
- In batch scripts, place the `source .../conda_init.sh` and `conda activate ...` lines after the `#BSUB` lines and before any other commands.
- To verify the environment, run `python -c "import sys; print(sys.executable)"`.

If `conda activate` fails:

- Check whether `python3` is already loaded with `module list`; if so, try `module unload python3`.
- Check whether `~/.bashrc` auto-loads another teaching environment that interferes with conda.

## Batch jobs on DTU HPC

Use `context_folder/template_bash.sh` as the canonical example for a normal batch script.

Typical pattern:

```bash
#!/bin/bash
#BSUB -J my_job
#BSUB -q hpc
#BSUB -n 4
#BSUB -W 10
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -M 2GB
#BSUB -o job_%J.out
#BSUB -e job_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python -u my_script.py
```

Common `#BSUB` fields:

- `-J`: job name shown in the queue.
- `-q`: queue, usually `hpc`.
- `-n`: number of CPU cores.
- `-W`: walltime limit in minutes.
- `-R "span[hosts=1]"`: keep cores on the same node.
- `-R "rusage[mem=2GB]"`: reserve memory per core.
- `-M 2GB`: hard memory limit per process.
- `-o` and `-e`: stdout and stderr files.
- Optional email flags such as `-u`, `-B`, and `-N`.
- Optional hardware selection such as `select[model==XeonGold6126]` when reproducibility matters.

Submission and inspection:

```bash
bsub < job.sh
```

Then inspect output files such as `job_<jobid>.out` and `job_<jobid>.err`.

## GPU jobs on DTU HPC

For GPU work, use the updated course environment:

```bash
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026
```

Do not use `02613` for GPU-topic code. The updated GPU workflow requires `02613_2026`.

Typical GPU batch pattern:

```bash
#!/bin/sh
#BSUB -q gpua100
#BSUB -J gpujob
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 00:30
#BSUB -R "select[gpu80gb]"
#BSUB -o batch_output/gpujob_%J.out
#BSUB -e batch_output/gpujob_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026

python gpuprogram.py
```

GPU-specific notes:

- Use queue `gpua100` for A100 GPUs.
- Request at least 4 CPU cores with `-n 4`.
- Request one GPU with `#BSUB -gpu "num=1:mode=exclusive_process"`.
- `exclusive_process` means the GPU is reserved for your process/job.
- Use `#BSUB -R "select[gpu80gb]"` when a specific GPU type is required.
- The example walltime is `00:30`; the slide notes GPU jobs can run up to 24 hours depending on the job setup and limits in the queue.
- Store output in a dedicated folder such as `batch_output/`.

When creating GPU scripts in this repo, prefer an explicit GPU-oriented shell script instead of reusing a CPU script unchanged.

## File transfer

Prefer terminal-based transfer.

Single-file upload from your own computer to HPC:

```bash
scp path/to/file.py <username>@login.hpc.dtu.dk:path/to/file.py
```

Single-file download from HPC to your own computer:

```bash
scp <username>@login.hpc.dtu.dk:path/to/file.py path/to/file.py
```

Interactive transfer for many files:

```bash
sftp <username>@transfer.gbar.dtu.dk
```

Useful `sftp` commands:

- `cd`, `ls`, `mkdir` for the remote side.
- `lcd`, `lls` for the local side.
- `put file.py` to upload.
- `get file.py` to download.
- `get *` to download many files.

Important:

- Run `scp` and `sftp` from your own computer, not from inside an active HPC shell.
- If you are not on DTU Wi-Fi, you may need VPN or SSH key setup.

## Guidance for future Codex sessions

For new weekly assignments:

1. Check whether the relevant `weekN/` folder already exists.
2. If not, create it using the existing naming convention.
3. Place assignment files directly in that folder unless there is a strong reason not to.
4. If a batch script is needed, base it on `context_folder/template_bash.sh`.
5. If the task involves GPU code, prefer `conda activate 02613_2026`.

Use `context_folder/` for deeper reference if details are missing, especially:

- `context_folder/template_bash.sh`
- `context_folder/initializing_conda_env`
- `context_folder/File transfer tofrom HPC.html`
