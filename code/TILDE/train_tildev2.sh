#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=agvaluate_finetuning
#SBATCH -n 1
#SBATCH --mem-per-cpu=8G
#SBATCH -o logs/print_agvaluate_finetuning.txt
#SBATCH -e logs/error_agvaluate_finetuning.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=10


module load anaconda/3.6
source activate <path_to_conda_environment>
module load cuda/10.0.130
module load gnu/5.4.0
module load mvapich2

HARD=TILDE_200_bm25
CKPT=5epoch

python train_tildev2.py \
  --output_dir <model_output_dir> \
  --model_name ielab/TILDEv2-TILDE200-exp \
  --save_steps 50000 \
  --train_dir <path_to_agvaluate-tilde-train-feats> \
  --q_max_len 16 \
  --p_max_len 192 \
  --fp16 \
  --per_device_train_batch_size 8 \
  --train_group_size 8 \
  --warmup_ratio 0.1 \
  --learning_rate 5e-6 \
  --num_train_epochs 20 \
  --overwrite_output_dir \
  --dataloader_num_workers 16 \
  --cache_dir ./cache