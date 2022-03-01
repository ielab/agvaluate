#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=agvaluate-ance-indexing
#SBATCH -n 1
#SBATCH --mem-per-cpu=10G
#SBATCH -o ../../data/logs/print_indexing.txt
#SBATCH -e ../../data/logs/error_indexing.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=10

module load anaconda/3.6
source activate <path_to_conda_environment>
module load cuda/10.2
module load gnu/5.4.0
module load mvapich2

# define this environment variable so pyserini can load
# the model from the cache instead of downloading it everytime
export PYSERINI_CACHE=<path_to_cache>

python ance_index_embedding_generator.py \
  --encoder castorini/ance-msmarco-passage \
  --corpus ../../data/all_json/passage-3-combined-24052021 \
  --index ../../data/<output_dir_agvaluate_ance_passage_index>
  