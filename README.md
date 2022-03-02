# Ag-valuate

Ag-valuate is a new test collection for both passage and document retrieval in the Agriculture domain.

Two sources of agricultural information were obtained as part of the collection: 1,878 agricultural reports from the [Grains Research Development Corporation](https://grdc.com.au/) and [State Departments of Agriculture in Australia](https://www.daf.qld.gov.au/); and 90,516 scientific journal and conference articles from 33 agricultural journals. These selected reports and journal articles were considered relevant to the grains industry and focused on crop agronomy and soils. The targeted subject matter related to the growth and management of grains crops including cereals (e.g. wheat, barley, and sorghum), legumes (e.g. chickpea, soybean, mungbean), and oilseeds (e.g. canola), and the management of the soils on which these crops are grown. Topics covered included recommendations and research relevant to the management of individual crops through varietals selection, sowing times, planting rates and row spacing etc; whole farming system performance, crop sequencing and fallow management practices; fertiliser management; and the identification and management of pest and diseases that affected the  grains industry. Both these sources came in the form of PDF documents.

The PDF reports are provided freely in the repository. The journal articles come from subscription journals so cannot be redistributed; however, we provide crawler scripts that can be used to download the full text using an institutional or paid subscription to these journals.

Once full-text PDFs were obtained, they were converted from PDF to JSON using Apache Tika. From here, the documents were further split into passages of three sentences (the Spacy sentencizer was used to derive sentence boundaries and code is provided for this.) From the 92,394 documents, 9,441,693 passages were produced.

A total of 210 topics were created from 165 documents (multiple, different topics could sometimes be derived from a single document). Topics were divided into training and test sets. The 50 topics with the most relevance assessments formed the test set and the remaining 160 topics formed the training set. (Other splits can be done as desired; ours was purely done for our experiments.) Each topic contained multiple query variations, a natural language question and an expert-authored answer, thus providing a rich representation of the information need. Relevance assessment by two agricultural experts produced 3,948 question-passage judged pairs.

Ag-valuate provides a rich resource with a wide variety of uses: passage or document retrieval, query variation, answer generation, scientific document extraction, and domain specific or expert search. To demonstrate the utility of Ag-valuate, we conducted experiments for two of these tasks, passage retrieval and query variation, using state-of-the-art neural rankers, reporting the effectiveness and providing the code with the collection.

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg