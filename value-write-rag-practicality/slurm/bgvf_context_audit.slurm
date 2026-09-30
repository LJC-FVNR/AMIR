#!/bin/bash
#SBATCH --job-name=vw_ctx_audit
#SBATCH --account=bgvf-dtai-gh
#SBATCH --partition=ghx4-interactive
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --gpus-per-node=1
#SBATCH --gpu-bind=verbose,closest
#SBATCH --time=01:00:00
#SBATCH --output=/work/nvme/bgvf/ywang151/value-write-rag-practicality/logs/%x_%j.out
#SBATCH --error=/work/nvme/bgvf/ywang151/value-write-rag-practicality/logs/%x_%j.err

set -euo pipefail

REPO_ROOT=/work/nvme/bgvf/ywang151/value-write-rag-practicality
cd "$REPO_ROOT"
mkdir -p logs results/context_scaling

module load default
source /sw/user/python/miniforge3-pytorch-2.10.0/etc/profile.d/conda.sh
conda activate base

export HF_HOME=/work/nvme/bgvf/ywang151/hf_cache
export HF_HUB_OFFLINE=1
export HF_DATASETS_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS=16

python -V
nvidia-smi
python -c "import torch, transformers; print('torch', torch.__version__, 'transformers', transformers.__version__, 'cuda', torch.cuda.is_available())"

srun python -u scripts/audit_final_query_extractor.py --max-examples 3
