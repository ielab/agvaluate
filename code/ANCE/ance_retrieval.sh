#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=agvaluate-ance-retrieval
#SBATCH -n 1
#SBATCH --mem-per-cpu=10G
#SBATCH -o ../../data/logs/print_retrieval.txt
#SBATCH -e ../../data/logs/error_retrieval.txt
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

python -m pyserini.dsearch \
  --index ../../data/<path_to_agvaluate_ance_passage_index> \
  --topics ../../data/queries/agask_questions-test50.tsv \
  --encoder castorini/ance-msmarco-passage \
  --output ../../data/runs/run-ANCE-agask-question-test50.tsv \
  --output-format msmarco \
  --batch-size 36 --threads 12

# convert to trec_eval format
python -m pyserini.eval.convert_msmarco_run_to_trec_run \
    --input ../../data/runs/run-ANCE-agask-question-test50.tsv \
    --output ../../data/runs/run-ANCE-agask-question-test50.trec

python -m pyserini.dsearch \
  --index ../../data/<path_to_agvaluate_ance_passage_index> \
  --topics ../../data/queries/agask_query-test50.tsv \
  --encoder castorini/ance-msmarco-passage \
  --output ../../data/runs/run-ANCE-agask-query-test50.tsv \
  --output-format msmarco \
  --batch-size 36 --threads 12

# convert to trec_eval format
python -m pyserini.eval.convert_msmarco_run_to_trec_run \
    --input ../../data/runs/run-ANCE-agask-query-test50.tsv \
    --output ../../data/runs/run-ANCE-agask-query-test50.trec
