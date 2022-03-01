#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=agvaluate_indexing
#SBATCH -n 1
#SBATCH --mem-per-cpu=15G
#SBATCH -o ../../data/logs/print_agvaluate_tilde-v2_indexing.txt
#SBATCH -e ../../data/logs/error_agvaluate_tilde-v2_indexing.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=10


module load anaconda/3.6
source activate <path_to_conda_environment>
module load cuda/10.0.130
module load gnu/5.4.0
module load mvapich2

python3 indexingv2.py \
--ckpt_path_or_name ../../data/<path_to_fine_tuned_agvaluate_tilde_v2_model> \
--collection_path ../../data/<path_to_expanded_passage_collection> \
--output_path ../../data/<expanded_index_output_dir>
