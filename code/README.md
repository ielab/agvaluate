# Ag-valuate Codebase

## Document Crawlers

This directory includes crawlers for Ag-valuate collection and pre-processing to convert PDFs to JSON and chunk documents into passages.

## Retrieval Models

We share the code for the retrieval and reranking models that were considered in the paper and required customisation. These include ANCE, BERT and TILDE. Other models such as BM25 and BM25+RM3 are used off the shelf.

## Fusion of Pools

`for_assigned_query_pool.py` is the rank fusion script used to form the pool of passages for judgements.

## Utils

- `agvaluate_eval.sh` is the evaluation script used to generate the results in this paper. It requires trec_eval.

- `extract_articles_dois.py` is a utility script to extract the DOIs of the documents in the collection from JSON files.
