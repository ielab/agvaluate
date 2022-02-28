import json
import os
from tqdm import tqdm
import spacy

nlp = spacy.blank("en")
nlp.add_pipe(nlp.create_pipe("sentencizer"))

IN_DIR = '../../../data/all_json/document'


def split_document_into_passage(document, num):
    passages = []
    doc = nlp(document)
    sentences = [sent.string.strip() for sent in doc.sents]
    chunks = list(chunk(sentences, num))
    for c in chunks:
        passages.append(' '.join(c))
    return passages


def chunk(sentences, chunk_size):
    for i in range(0, len(sentences), chunk_size):
        yield sentences[i:i + chunk_size]


def main():

    line_count = 0
    file_count = 0

    total_file = sum(1 for _ in os.listdir(IN_DIR))
    for filename in tqdm(os.listdir(IN_DIR), total=total_file):
        file_path = os.path.join(IN_DIR, filename)
        if filename == '.DS_Store':
            continue
        else:
            json_contents = json.loads(open(file_path, 'r').read())
            report_id = json_contents["report_id"]
            content = json_contents["text"]
            passages = split_document_into_passage(content, 3)
            for index, p in enumerate(passages):
                content = {
                    "report_id": f'{report_id}-{index+1}',
                    "type": json_contents["type"],
                    "project_number": json_contents["project_number"],
                    "report_title": json_contents["report_title"],
                    "region_name": json_contents["region_name"],
                    "category_name": json_contents["category_name"],
                    "research_theme_name": json_contents["research_theme_name"],
                    "organisation_name": json_contents["organisation_name"],
                    "complete_date": json_contents["complete_date"],
                    "supervisor_name": json_contents["supervisor_name"],
                    "publish_date": json_contents["publish_date"],
                    "report_path": json_contents["report_path"],
                    "keywords": json_contents["keywords"],
                    "pdf_url": json_contents["pdf_url"],
                    "web_url": json_contents["web_url"],
                    "text": p,
                    "summary": json_contents["summary"]
                }
                if line_count < 1000000:
                    line_count += 1
                    out = open(f'../../../data/all_json/passage-3-combined-24052021/passage-3-{file_count}.jsonl', 'a+')
                    out.write(f'{json.dumps(content)}\n')
                else:
                    line_count = 1
                    file_count += 1
                    out = open(f'../../../data/all_json/passage-3-combined-24052021/passage-3-{file_count}.jsonl', 'a+')
                    out.write(f'{json.dumps(content)}\n')

if __name__ == '__main__':
    main()
