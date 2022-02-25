import json
import subprocess
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
from tika import parser
import spacy
import re

nlp = spacy.blank("en")
nlp.add_pipe(nlp.create_pipe("sentencizer"))

IN_PATH = 'Reindex'
DOC_OUT_PATH = 'Reindex_json/document'
PASS_OUT_PATH = 'Reindex_json/passage-3'

def chunk(sentences, chunk_size):
    for i in range(0, len(sentences), chunk_size):
        yield sentences[i:i + chunk_size]

def split_document_into_passage(document):
    passages = []
    doc = nlp(document)
    sentences = [sent.string.strip() for sent in doc.sents]
    chunks = list(chunk(sentences, 3))
    for c in chunks:
        passages.append(' '.join(c))
    return passages

def extractPDF(path):
    raw = parser.from_file(path)
    if raw['content']:
        return raw['content'].strip()
    else:
        return None

valid_pdfs = [f for f in listdir(IN_PATH) if isfile(join(IN_PATH, f)) and not f.startswith('.')]

for pdf_name in tqdm(valid_pdfs):
    if pdf_name == '150705.pdf':
        title = 'Advanced Techniques for Managing Subsoil Constraints'
    elif pdf_name == '150703.pdf':
        title = 'Informed carbon strategies on mixed farms: practices and carbon compared'
    elif pdf_name == '20201020.pdf':
        title = 'Quantifying the effectiveness of cover crops to increase water infiltration and reduce evaporation in the northern region'
    else:
        pdf_path = join(IN_PATH, pdf_name)
        raw_pdf_title = subprocess.run(['pdftitle','-p',pdf_path], stdout=subprocess.PIPE)
        title = raw_pdf_title.stdout.decode('utf-8').strip()
    doc_out_name = '{}.json'.format(pdf_name.split('.')[0])

    text = extractPDF(join(IN_PATH, pdf_name))
    text = text.replace('\n', ' ')
    text = re.sub(' +', ' ', text)

    ##########################
    # Generate Document JSON #
    ##########################

    # json_obj = {
    #     "report_id": pdf_name.split('.')[0],
    #     "type": "report",
    #     "project_number": pdf_name.split('.')[0],
    #     "report_title": title,
    #     "region_name": "N/A",
    #     "category_name": "GRDC Research",
    #     "research_theme_name": "GRDC Research",
    #     "organisation_name": "GRDC",
    #     "complete_date": "N/A",
    #     "supervisor_name": "N/A",
    #     "publish_date": "N/A",
    #     "report_path": f'data/reports/{pdf_name}',
    #     "keywords": [],
    #     "pdf_url": "N/A",
    #     "web_url": "N/A",
    #     "text": text,
    #     "summary": ""
    # }

    # open(join(DOC_OUT_PATH, doc_out_name), 'w+').write(json.dumps(json_obj))

    #########################
    # Generate Passage JSON #
    #########################

    passages = split_document_into_passage(text)

    for ind, passage in enumerate(passages):
        json_obj = {
            "report_id": '{}-{}'.format(pdf_name.split('.')[0], ind + 1),
            "type": "report",
            "project_number": pdf_name.split('.')[0],
            "report_title": title,
            "region_name": "N/A",
            "category_name": "GRDC Research",
            "research_theme_name": "GRDC Research",
            "organisation_name": "GRDC",
            "complete_date": "N/A",
            "supervisor_name": "N/A",
            "publish_date": "N/A",
            "report_path": f'data/reports/{pdf_name}',
            "keywords": [],
            "pdf_url": "N/A",
            "web_url": "N/A",
            "text": passage,
            "summary": ""
        }
        pass_out_name = '{}-{}.json'.format(pdf_name.split('.')[0], ind + 1)

        open(join(PASS_OUT_PATH, pass_out_name), 'w+').write(json.dumps(json_obj))