# Ag-valuate Document Crawler

Contains code to download the documents for Ag-valuate: both GRDC reports and journals.

## Requirements

```
requests
json
os
wget
time
tika
spacy
math
bs4
random
```

## Run

The steps are:

1. Download GRDC reports from API. Code is in `./grdc_reports`.
```
python3 main.py -d
```
OR
```
python3 main.py --download
```

2. Convert PDF to JSON files
```
python3 main.py -e
```
OR
```
python3 main.py --extract
```
Example JSON file for each report:

```
{
  "report_id": "",
  "project_number": "",
  "report_title": "",
  "region_name": "",
  "category_name": "",
  "research_theme_name": "",
  "organisation_name": "",
  "commence_date": "",
  "complete_date": "",
  "state": "",
  "supervisor_name": "",
  "report_type": "",
  "report_status": "",
  "publish_date": "",
  "report_summary": "",
  "keywords": "",
  "pdf_url": "",
  "web_url": "",
  "html_content": "",
  "report_achievement": "",
  "report_conclusion": "",
  "report_outcome": "",
  "report_recommendation": "",
  "report_discussion": "",
  "other_research": "",
  "ip_summary": "",
  "additional_information": "",
  "report_full_text_content": "",
  "attachments": [
    {
      "report_id": "",
      "attachment_url": "",
      "attachment_id": "",
      "attachment_name": "",
      "attachment_size": "",
      "attachment_type": "",
      "attachment_base64_content": "",
      "attachment_full_text_content": ""
    }
  ]
}
```

Report 1030 contains a zipped file as one of the attachments, which contains 10 doc files inside, this is a special case and need to be handled carefully.

3. Clean json file to remove uneeded content
```
python3 main.py -c
```
OR
```
python3 main.py --clean
```

4. Split content to meet the field lenght in pyserini
```
python3 main.py -s
```
OR
```
python3 main.py --split
```

5. Add some extra reports that require special handling
```
python3 add_new_reports_for_index.py
```

### Reports directory structure

All reports, pdf, attachments will be downloaded automatically in reports directory.

Inside reports directory:

```
/reports
.../1                                               ----> report_id
    .../html/web.txt                                ----> html content of the report webpage
    .../pdf/xxx.pdf                                 ----> pdf version of the report
    .../attachment/xxx(.docx)(.doc)(.pdf)(.txt)     ----> all attachments for the report, in different file formats
    .../json/1.json                                 ----> JSON file for each report and their attachments, file name is report ID
```

### Config

`Config.json` contains all the APIs provided by GRDC, for details of usage, please visit https://grdcfinalreports.cerdi.edu.au/api/docs/

### Reports

Reports stored at TBC 

JSON Reports stored at https://github.com/ielab/agvaluate/tree/main/data/grdc_reports_json

6. Download journal articles

### Config

`Config.json` replace all API keys with you institutional or paid subscription. Elsevier and Springer might have multiple keys.

Run each crawler script, e.g.
```
python3 elsevier_crawler.py
```

7. Clean JSON files to keep ONLY the metadata that exists in both reports and journal articles
```
python3 grdc_reports/generate_valid_json_for_report_and_journal.py
```

8. Split documents into passages
```
python3 grdc_reports/split_doc_into_para.py
```

Example JSON file for each passage (2 sentences) level for document:

```
{
  "pid": "report_id-index" # for each passage in a document, increment the index by 1
  "report_id": "",
  "project_number": "",
  "report_title": "",
  "region_name": "",
  "category_name": "",
  "research_theme_name": "",
  "organisation_name": "",
  "commence_date": "",
  "complete_date": "",
  "state": "",
  "supervisor_name": "",
  "report_type": "",
  "report_status": "",
  "publish_date": "",
  "keywords": "",
  "pdf_url": "",
  "web_url": "",
  "passage": ""
```

Example JSON file for each passage (2 sentences) level for attachment:

```
{
  "pid": "report_id-attachment_id-index" # for each passage in an attachment, increment the index by 1
  "report_id": "attachment_id",
  "project_number": "",
  "report_title": "attachment_name",
  "region_name": "",
  "category_name": "",
  "research_theme_name": "",
  "organisation_name": "",
  "commence_date": "",
  "complete_date": "",
  "state": "",
  "supervisor_name": "",
  "report_type": "attachment_type",
  "report_status": "",
  "publish_date": "",
  "keywords": "",
  "pdf_url": "attachment_url",
  "web_url": "attachment_url",
  "passage": ""
```
