# Ag-valuate
## A Test Collection for Agricultural Information Needs

### Table of Contents
<ol>
  <li><a href="#paper">Paper</a></li>
  <li><a href="#overview">Overview</a></li>
  <li><a href="#documents-and-passages">Documents and Passages</a></li>
  <li><a href="#questionquery-topics">Question/Query Topics</a></li>
  <li><a href="#pooling-and-relevance-assessment">Pooling and Relevance Assessment</a></li>
  <li><a href="#passage-retrieval-baselines">Passage Retrieval Baselines</a></li>
</ol>

## Paper

This work is currently under review as a resource paper at CIKM 2022.

```
@inproceedings{mourad2022agvaluate,
 title={Ag-valuate: A Test Collection for Agricultural Information Needs},
 author={Mourad, Ahmed and Koopman, Bevan and Li, Hang and Vegt, Anton van der and Zhuang, Shengyao and Gibon, Simon and Dang, Yash and Lawrence, David and Zuccon, Guido},
 booktitle={},
 year={2022}
}
```

## Overview

Ag-valuate is a new test collection for both passage and document retrieval in the Agriculture domain.

Two sources of agricultural information were obtained as part of the collection: 4,003 agricultural reports from the [Grains Research Development Corporation](https://grdc.com.au/) and [State Departments of Agriculture in Australia](https://www.daf.qld.gov.au/); and 82,843 scientific journal and conference articles from 33 agricultural journals.

These selected reports and journal articles were considered relevant to the grains industry and focused on crop agronomy and soils. The targeted subject matter related to the growth and management of grains crops including cereals (e.g. wheat, barley, and sorghum), legumes (e.g. chickpea, soybean, mungbean), and oilseeds (e.g. canola), and the management of the soils on which these crops are grown. Topics covered included recommendations and research relevant to the management of individual crops through varietals selection, sowing times, planting rates and row spacing etc; whole farming system performance, crop sequencing and fallow management practices; fertiliser management; and the identification and management of pest and diseases that affected the  grains industry. Both these sources came in the form of PDF documents.

Ag-valuate provides a rich resource with a wide variety of uses: passage or document retrieval, query variation, answer generation, scientific document extraction, and domain specific or expert search. To demonstrate the utility of Ag-valuate, we conducted experiments for two of these tasks, passage retrieval and query variation, using state-of-the-art neural rankers, reporting the effectiveness and providing the code with the collection.

## Documents and Passages

The pre-processed [GRDC JSON reports](https://github.com/ielab/agvaluate/tree/main/data/grdc_reports_json) are provided freely in the repository. The raw PDF files of the GRDC reports can be downloaded from [here](https://doi.org/10.48610/0160dc7). The journal articles come from subscription journals so cannot be redistributed. However, we provide crawler scripts that can be used to download the full collection using a public API for the reports and an institutional or paid subscription to these journals. The [Document Crawler](https://github.com/ielab/agvaluate/tree/main/code/DocumentCrawler) includes details of how to run the following document crawlers:

<ol>
  <li><a href="https://github.com/ielab/agvaluate/tree/main/code/DocumentCrawler/grdc_reports">GRDC Reports</a></li>
  <li><a href="https://github.com/ielab/agvaluate/blob/main/code/DocumentCrawler/journals/elsevier_crawler.py">Elsevier</a></li>
  <li><a href="https://github.com/ielab/agvaluate/blob/main/code/DocumentCrawler/journals/mdpi_crawler.py">MDPI</a></li>
  <li><a href="https://github.com/ielab/agvaluate/blob/main/code/DocumentCrawler/journals/springer_crawler.py">Springer</a></li>
  <li><a href="https://github.com/ielab/agvaluate/blob/main/code/DocumentCrawler/journals/wiley_crawler.py">Wiley</a></li>
</ol>

Once full-text PDFs were obtained, they were converted from PDF to JSON using [Apache Tika](https://github.com/chrismattmann/tika-python). From here, the documents were further split into passages of three sentences (the Spacy sentencizer was used to derive sentence boundaries and [\[Code\]](https://github.com/ielab/agvaluate/blob/main/code/DocumentCrawler/grdc_reports/split_doc_into_para.py).) From the 86,846 documents, 9,441,693 passages were produced.

## Question/Query Topics

A total of 210 topics were created from 165 documents (multiple, different topics could sometimes be derived from a single document). Topics were divided into training and test sets. The 50 topics with the most relevance assessments formed the test set and the remaining 160 topics formed the training set. (Other splits can be done as desired; ours was purely done for our experiments.) Each topic contained multiple query variations, a natural language question and an expert-authored answer, thus providing a rich representation of the information need. Relevance assessment by two agricultural experts produced 3,948 question-passage judged pairs.

![image](https://user-images.githubusercontent.com/15306828/156973458-767088e1-3047-414e-ab57-07c97f1b9096.png)

## Pooling and Relevance Assessment

Using the 210 topics we set out to form a high quality pool for relevance assessment. We considered two state-of-the-art neural ranking systems:

<ol>
  <li><a href="https://github.com/ielab/agvaluate/tree/main/code/BERT">monoBERT Reranker</a>, involving a first stage BM25 initial retrieval of 1000 documents, followed by a fine-tuned monoBERT reranker without interpolating with the BM25. We used a monoBERT model pre-trained on the MSMARCO dataset and then fine-tuned on the 160 training topics.</li>
  <li><a href="https://github.com/ielab/agvaluate/tree/main/code/TILDE">TILDEv2 Tuned</a>, is a neural reranker that utilises document expansion at indexing time to avoid the need for neural encoding of query or document at query time. It involved a first stage BM25 retrieval of 1000 documents, followed by a fine-tuned TILDEv2 reranker. TILDEv2 was added as a computationally efficient --- yet still effective --- model that might be deployed in a live search system. This model was also fine-tuned on the 160 training topics.</li>
</ol>

Runs for all 210 topics were produced for each of the two systems above. These runs were fused using reciprocal rank fusion to produce the final pool for human assessment. [\[Code\]](https://github.com/ielab/agvaluate/blob/main/code/form_assigned_query_pool.py)

Relevance assessment was conducted by authors D.Lawrence and Y.Dang, both agricultural scientists. Each was presented with the topic question, a list of passages for judging, along with a link to the PDF source document from which the passage was extracted. Grades of relevance were: relevant, marginal and non-relevant. The criterion for relevance given to assessors was: `does the passage help to answer the question`, where `relevant` meant that the passage contained the answer, `marginal` meant  the passage contained some part but not the whole answer, and `non-relevant` meant the passage contained no useful information.

For the topics from the test set, assessors judged in order until rank 20; if no relevant passage was found in the top 20 then they continued down the ranking until a relevant passage was found or rank 100 was reached.

For the topics from the training set, assessors judged the top 10 passages, regardless of relevance. Topics obtained via the known-item retrieval process will have at least 1 relevant passage.

![image](https://user-images.githubusercontent.com/15306828/156983246-bbf3c85d-20d3-43ed-afc8-1c7a9a2655e8.png)

## Passage Retrieval Baselines

We implemented the following retrieval models and evaluated them on the Ag-valuate test collection:

<ol>
  <li><strong>BM25</strong>, Vanilla BM25 baseline to understand how a simple term-based retrieval performs.</li>
  <li><strong>BM25-Tuned-RM3</strong>, A BM25 with params <em>b</em> and <em>k1</em> tuned on the training set and pseudo relevance feedback using RM3.</li>
  <li><a href="https://github.com/ielab/agvaluate/tree/main/code/BERT">monoBERT Reranker</a>, BM25 followed by a monoBERT reranker pre-trained on MSMARCO and fine-tuned on the 160 training topics. (The same system used for pooling.)</li>
  <li><a href="https://github.com/ielab/agvaluate/tree/main/code/TILDE">TILDEv2 Tuned</a>, The same computationally efficient neural document expansion model used for pooling. </li>
  <li><a href="https://github.com/ielab/agvaluate/tree/main/code/TILDE">TILDEv2</a>, TILDEv2 without fine-tuning on the target domain, providing an estimate of the benefit of performing fine-tuning.</li>
  <li><a href="https://github.com/ielab/agvaluate/tree/main/code/ANCE">ANCE</a>, is a dense retriever that selects more realistic negative training instances from an Approximate Nearest Neighbor (ANN) index of the corpus. We used a ANCE model pre-trained on the MSMARCO dataset.</li>
</ol>

To make use of the multi-faceted topics provided by Ag-valuate, we ran the above models using both the natural language questions and keyword query versions of the topic. This aimed to uncover some insights into how query variation impact effectiveness.

![image](https://user-images.githubusercontent.com/15306828/156983494-b2d291dc-cc30-465f-81bd-62ee39f62af9.png)

Shield: [![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
