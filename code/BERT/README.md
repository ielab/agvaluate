# Ag-valuate BERT Reranker

### Step 1 - Create feature file

First create the feature JSON file:

```bash
python helpers/build_train_from_ranking_agask.py \
  --tokenizer_name nboost/pt-bert-large-msmarco \
  --qrel qrels/qrel-known_item-passage.tsv \
  --json_dir feature_json \
  --query_collection queries/agask_questions-train_not50.csv \
  --doc_collection docs/agask_docs.csv
```

This will create `feature_json/agask_docs.features.json` which is used for training. 


### Setep 2 - train/eval model

```zsh
python3 run_agask.py \
  --save_steps 2000 \
  --max_len 512 \
  --cache_dir cache\
  --per_device_train_batch_size 2 \
  --train_group_size 2 \
  --gradient_accumulation_steps 2 \
  --weight_decay 0.01 \
  --learning_rate 1e-6 \
  --num_train_epochs 10 \
  --dataloader_num_workers 8 \
  --fp16 \
  --do_train \
  --output_dir models/agask_model \
  --model_name_or_path nboost/pt-bert-large-msmarco \
  --train_dir feature_json \
  --overwrite_output_dir
```

This will train the pytorch model and write it out to `{models/agask_model`.

### Step 3 - run the model

Run the model via:


```zsh
python bert_reranker.py \
	--run_file examples/agask/runs/injected-run-bm25-agask-questions-test50.res \
	--collection_file examples/agask/collection/agask_collection.tsv \
	--query_file examples/agask/queries/agask_questions-test50.csv \
	--model_name_or_path examples/agask/models/agask_model \
	--tokenizer_name_or_path examples/agask/models/agask_model \
	--batch_size 32 \
	--cut_off 500
``````

This will rerank the top `--cut_off` documents from `--run_file` using queries from `--query_file` and model `--model_name_or_path`.

The resulting ranking will be written to a new file with name:

`run-query_{query_file}-stage1_{run_file}-model_{model_name_or_path}-cut_{cut_off}.res`
