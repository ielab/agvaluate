#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=agvaluate-expanding
#SBATCH -n 1
#SBATCH --mem-per-cpu=5G
#SBATCH -o ../../data/logs/print_expanding.txt
#SBATCH -e ../../data/logs/error_expanding.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8

module load anaconda/3.6
source activate <path_to_conda_environment>
module load cuda/10.0.130
module load gnu/5.4.0
module load mvapich2


python expansion.py \
  --corpus_path ../../data/<path_to_passage_collection_tsv> \
  --output_dir ../../data/<expanded_collection_output_dir>
  