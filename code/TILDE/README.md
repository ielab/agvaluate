# Ag-valuate TILDEv2 Reranker

This directory contains the shell scripts used to run the different steps of deploying TILDE (v1 and v2). These include expanding the collection, fine-tuning on Ag-valuate (training), indexing, and inference. First, you need to deploy [TILDE](https://github.com/ielab/TILDE).

### Step 1 - Expand the collection using TILDEv1

Run the shell script `expansion.sh`. It requires GPU access.
```
python expansion.py \
  --corpus_path ../../data/<path_to_passage_collection_tsv> \
  --output_dir ../../data/<expanded_collection_output_dir>
```

### Step 2 - Create feature file

Follow the same instructions for [Step 1 in the monoBERT Reranker](https://github.com/ielab/agvaluate/tree/main/code/BERT#step-1---create-feature-file).

### Step 2 - Fine-tune TILDEv2 on Ag-valuate

Re-train TILDE v2, that was initially fine-tuned on MS MARCO, by running the shell script `train_tildev2.sh`. It requires access to 1 GPU and 80GB of memory.
```
python train_tildev2.py \
  --output_dir ../../data/<model_output_dir> \
  --model_name ielab/TILDEv2-TILDE200-exp \
  --save_steps 50000 \
  --train_dir ../../data/<path_to_agvaluate-tilde-train-feats> \
  --q_max_len 16 \
  --p_max_len 192 \
  --fp16 \
  --per_device_train_batch_size 8 \
  --train_group_size 8 \
  --warmup_ratio 0.1 \
  --learning_rate 5e-6 \
  --num_train_epochs 20 \
  --overwrite_output_dir \
  --dataloader_num_workers 16 \
  --cache_dir ./cache
```

### Step 3 - Index the collection

Fine-tuned TILDE v2 is used for indexing, including scoring tokens per passage. Run the shell script `indexingv2.sh`. It requires access to 1 GPU and 150GB of memory.
```
python3 indexingv2.py \
--ckpt_path_or_name ../../data/<path_to_fine_tuned_agvaluate_tilde_v2_model> \
--collection_path ../../data/<path_to_expanded_passage_collection> \
--output_path ../../data/<expanded_index_output_dir>
```

### Step 4 - Run the model

Run the model via `inference.sh`. It requires access to 120GB of memory.
```
python3 inferencev2.py \
--index_path ../../data/<path_to_expanded_passage_collection> \
--query_path ../../data/queries/agask_questions-test50.csv \
--run_path ../../data/runs/run-bm25-agask-questions-test50.res \
--save_path ../../data/runs/run-TILDEv2-tuned-bm25-agask-questions-test50.txt

python3 inferencev2.py \
--index_path ../../data/<path_to_expanded_passage_collection> \
--query_path ../../data/queries/agask_questions-test50.csv \
--run_path ../../data/runs/run-bm25-rm3-agask-questions-test50.res \
--save_path ../../data/runs/run-TILDEv2-tuned-bm25-rm3-agask-questions-test50.txt
```
