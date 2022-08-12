#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=agvaluate_bert_feats
#SBATCH -n 1
#SBATCH --mem-per-cpu=8G
#SBATCH -o <local_directory>/agvaluate/data/logs/print_agvaluate_bert_feats.txt
#SBATCH -e <local_directory>/agvaluate/data/logs/error_agvaluate_bert_feats.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=5

# module load anaconda/3.6
source activate <local_directory>/.conda/envs/bert-reranker
module load cuda/10.0.130
module load gnu/5.4.0
module load mvapich2

python helpers/build_train_from_ranking_agask.py \
    --tokenizer_name nboost/pt-bert-large-msmarco \
    --qrel <local_directory>/agvaluate/data/qrels/qrel-known_item-passage.tsv \
    --json_dir <local_directory>/agvaluate/data/feature_json/agask_questions_train \
    --query_collection <local_directory>/agvaluate/data/queries/agask_questions-train_not50.csv \
    --doc_collection <local_directory>/agvaluate/data/docs/agask_docs.csv

