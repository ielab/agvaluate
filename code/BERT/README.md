# Ag-valuate BERT Reranker

This directory contains the shell scripts used to run the different steps of deploying monoBERT. These include fine-tuning on Ag-valuate (training) and inference. First, you need to deploy [Reranker](https://github.com/ielab/Reranker).

### Step 1 - Create feature file

First create the feature JSON file. You need to generate that for each of the training sets used. for example, we will create two for fine-tuning on each of the Natural Language Questions (NLQ) or the keyword queries (KQ). Go to the `Reranker` repo and run:

```bash
python examples/agask/helpers/build_train_from_ranking_agask.py \
  --tokenizer_name nboost/pt-bert-large-msmarco \
  --qrel <path to agvaluate>/data/qrels/qrel-known_item-passage.tsv \
  --json_dir feature_json/agask_question_train \
  --query_collection queries/agask_questions-train_not50.csv \
  --doc_collection docs/agask_docs.csv
```

This will create `feature_json/agask_question_train/agask_docs.features.json` which is used for training. 


### Setep 2 - train the model

```bash
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
  --output_dir <path to agvaluate>/data/models/BERT-NLQ \
  --model_name_or_path nboost/pt-bert-large-msmarco \
  --train_dir <path to agvaluate>/data/feature_json/agask_question_train \
  --overwrite_output_dir
```

This will train the pytorch model and write it out to `<path to agvaluate>/data/models/BERT-NLQ`.

### Step 3 - run the model

Run the model via:

```bash
python bert_reranker.py \
  --run_file <path to agvaluate>/data/runs/BM25/run-bm25-agask-questions-test50.res \
  --collection_file <path to agvaluate>/data/collections/agask_collection-all_docs.tsv \
  --query_file <path to agvaluate>/data/queries/agask_questions-test50.csv \
  --model_name_or_path <path to agvaluate>/data/models/BERT-NLQ \
  --tokenizer_name_or_path <path to agvaluate>/data/models/BERT-NLQ \
  --output_ranking <path to agvaluate>/data/runs/monoBERT-tuned-NLQ/run-monoBERT-tuned-agask-test50.txt \
  --batch_size 32 \
  --cut_off 500
``````

This will rerank the top `--cut_off` documents from `--run_file` using queries from `--query_file` and model `--model_name_or_path`.

The resulting ranking will be written to a new file with name `--output_ranking`.

**Note:** `agask_collection-all_docs.tsv` shall be generated once you successfully crawl the collection.