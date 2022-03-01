# Ag-valuate TILDEv2 Reranker

This directory contains the shell scripts used to run the different steps of deploying TILDE to AgAsk. These include expanding the collection, fine-tuning (training), indexing, and inference.

## Notes:
- For collection expansion, you must use [TILDE v1](huggingface.co/ielab/tilde).
- For fine-tuning, we retrain [TILDE v2](https://huggingface.co/ielab/TILDEv2-TILDE200-exp) that was initially fine-tuned on MS MARCO. Currently, TILDE v2 is fine-tuned on the relevance judgements of Agvaluate based on the passages extracted by Apache Tika PDF parser.
- Fine-tuned TILDE v2 is used for indexing, including scoring tokens per passage.
- Adding new passages requires re-expanding the collection and re-indexing.
- It is recommended to fine-tune TILDE v2 on the same collection deployed in production. However, we currently deploy a TILDE v2 model that was fine-tuned on the Tika collection to retrieve passages from a new collection built using PDFactor parser.
