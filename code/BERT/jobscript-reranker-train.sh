#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=agvaluate_bert_train_nlq
#SBATCH -n 1
#SBATCH --mem-per-cpu=8G
#SBATCH -o <local_directory>/agvaluate/data/logs/print_agvaluate_bert_train_nlq.txt
#SBATCH -e <local_directory>/agvaluate/data/logs/error_agvaluate_bert_train_nlq.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:tesla-smx2:1
#SBATCH --cpus-per-task=1

# module load anaconda/3.6
source activate <local_directory>/.conda/envs/bert-reranker
module load cuda/10.0.130
module load gnu/5.4.0
module load mvapich2

python run_agask.py \
  --save_steps 2000 \
  --max_len 512 \
  --cache_dir cache\
  --per_device_train_batch_size 2 \
  --train_group_size 6 \
  --gradient_accumulation_steps 2 \
  --weight_decay 0.01 \
  --learning_rate 1e-6 \
  --num_train_epochs 10 \
  --dataloader_num_workers 8 \
  --fp16 \
  --do_train \
  --output_dir <local_directory>/agvaluate/data/models/BERT-NLQ-KQ \
  --model_name_or_path <local_directory>/agvaluate/data/models/BERT-NLQ \
  --train_dir <local_directory>/agvaluate/data/feature_json/agask_query_train \
  --overwrite_output_dir