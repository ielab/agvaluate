#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=agvaluate_bert_reranker_nlq
#SBATCH -n 1
#SBATCH --mem-per-cpu=16G
#SBATCH -o <local_directory>/agvaluate/data/logs/print_agvaluate_bert_reranker_nlq.txt
#SBATCH -e <local_directory>/agvaluate/data/logs/error_agvaluate_bert_reranker_nlq.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:tesla-smx2:1
#SBATCH --cpus-per-task=1

# module load anaconda
source activate <local_directory>/.conda/envs/bert-reranker
module load cuda/10.0.130
module load gnu/5.4.0
module load mvapich2

python bert_reranker.py \
	--run_file <local_directory>/agvaluate/data/runs/BM25/run-bm25-agask-questions-test50.res \
	--collection_file <local_directory>/TILDE/data/collections/agask_collection-all_docs.tsv \
	--query_file <local_directory>/agvaluate/data/queries/agask_questions-test50.csv \
	--model_name_or_path <local_directory>/agvaluate/data/models/BERT-NLQ \
	--tokenizer_name_or_path <local_directory>/agvaluate/data/models/BERT-NLQ \
	--output_ranking <local_directory>/agvaluate/data/runs/monoBERT-tuned-NLQ/run-monoBERT-tuned-agask-test50.txt \
	--batch_size 32 \
	--cut_off 500

python bert_reranker.py \
	--run_file <local_directory>/agvaluate/data/runs/BM25/run-bm25-tuned-rm3-agask-questions-test50.res \
	--collection_file <local_directory>/TILDE/data/collections/agask_collection-all_docs.tsv \
	--query_file <local_directory>/agvaluate/data/queries/agask_questions-test50.csv \
	--model_name_or_path <local_directory>/agvaluate/data/models/BERT-NLQ \
	--tokenizer_name_or_path <local_directory>/agvaluate/data/models/BERT-NLQ \
	--output_ranking <local_directory>/agvaluate/data/runs/monoBERT-tuned-NLQ/run-monoBERT-tuned-agask-test50-tuned-rm3.txt \
	--batch_size 32 \
	--cut_off 500

python bert_reranker.py \
	--run_file <local_directory>/agvaluate/data/runs/BM25/run-bm25-agask-query-test50.res \
	--collection_file <local_directory>/TILDE/data/collections/agask_collection-all_docs.tsv \
	--query_file <local_directory>/agvaluate/data/queries/agask_query-test50.csv \
	--model_name_or_path <local_directory>/agvaluate/data/models/BERT-NLQ \
	--tokenizer_name_or_path <local_directory>/agvaluate/data/models/BERT-NLQ \
	--output_ranking <local_directory>/agvaluate/data/runs/monoBERT-tuned-NLQ/run-monoBERT-tuned-agask-query-test50.txt \
	--batch_size 32 \
	--cut_off 500

python bert_reranker.py \
	--run_file <local_directory>/agvaluate/data/runs/BM25/run-bm25-tuned-rm3-agask-query-test50.res \
	--collection_file <local_directory>/TILDE/data/collections/agask_collection-all_docs.tsv \
	--query_file <local_directory>/agvaluate/data/queries/agask_query-test50.csv \
	--model_name_or_path <local_directory>/agvaluate/data/models/BERT-NLQ \
	--tokenizer_name_or_path <local_directory>/agvaluate/data/models/BERT-NLQ \
	--output_ranking <local_directory>/agvaluate/data/runs/monoBERT-tuned-NLQ/run-monoBERT-tuned-agask-query-test50-tuned-rm3.txt \
	--batch_size 32 \
	--cut_off 500