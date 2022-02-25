#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=agvaluate_inference
#SBATCH -n 1
#SBATCH --mem-per-cpu=30G
#SBATCH -o logs/print_inference.txt
#SBATCH -e logs/error_inference.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:0
#SBATCH --cpus-per-task=4


module load anaconda/3.6
source activate <path_to_conda_environment>
module load cuda/10.0.130
module load gnu/5.4.0
module load mvapich2

python3 inferencev2.py \
--index_path <path_to_expanded_passage_collection> \
--query_path ../../data/queries/agask_questions-test50.csv \
--run_path ../../data/runs/run-bm25-agask-questions-test50.res \
--save_path ../../data/runs/run-TILDEv2-tuned-bm25-agask-questions-test50.txt

python3 inferencev2.py \
--index_path <path_to_expanded_passage_collection> \
--query_path ../../data/queries/agask_questions-test50.csv \
--run_path ../../data/runs/run-bm25-rm3-agask-questions-test50.res \
--save_path ../../data/runs/run-TILDEv2-tuned-bm25-rm3-agask-questions-test50.txt

python3 inferencev2.py \
--index_path <path_to_expanded_passage_collection> \
--query_path ../../data/queries/agask_query-test50.csv \
--run_path ../../data/runs/run-bm25-agask-query-test50.res \
--save_path ../../data/runs/run-TILDEv2-tuned-bm25-agask-query-test50.txt

python3 inferencev2.py \
--index_path <path_to_expanded_passage_collection> \
--query_path ../../data/queries/agask_query-test50.csv \
--run_path ../../data/runs/run-bm25-rm3-agask-query-test50.res \
--save_path ../../data/runs/run-TILDEv2-tuned-bm25-rm3-agask-query-test50.txt