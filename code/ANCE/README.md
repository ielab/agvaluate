# Ag-valuate ANCE Dense Retriever

### Step 1 - Index the collection

Generate embeddings for the entire collection using pyserini pre-trained ANCE encoder and store in FAISS index. Run the shell script `ance_index_embedding_generator.sh`. It requires GPU access.

```
python ance_index_embedding_generator.py \
  --encoder castorini/ance-msmarco-passage \
  --corpus <path_to_passage_collection_jsonl> \
  --index <output_dir_passage_index>
```

### Step 2 - Convert Query IDs from HashString to Integers (required by pyserini) and save into tsv

Pass a list of one or more query files, e.g.

```
python format_input hash2int data/query/agask_questions-test50.csv
```

It will generate a file with the same name and in tsv format

### Setep 3 - Run the model

Run the model via `ance_retrieval.sh`. It requires GPU access.

```
python -m pyserini.dsearch \
  --index <path_to_agvaluate_ance_passage_index> \
  --topics ../../data/queries/agask_questions-test50.tsv \
  --encoder castorini/ance-msmarco-passage \
  --output ../../data/runs/run-ANCE-agask-question-test50.tsv \
  --output-format msmarco \
  --batch-size 36 --threads 12
```

Convert the output to trec_eval format

```
python -m pyserini.eval.convert_msmarco_run_to_trec_run \
    --input ../../data/runs/run-ANCE-agask-question-test50.tsv \
    --output ../../data/runs/run-ANCE-agask-question-test50.trec
```

### Step 4 - Convert Query IDs in the runs from Integer back to HashStrings

Pass a list of one or more query / run files, e.g.

```
python format_input int2hash data/query/agask_questions-test50.csv run-ANCE-agask-question-test50.bf.trec
```

It will generate a file with the same name and in txt format
