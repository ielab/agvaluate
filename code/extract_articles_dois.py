import json
import os
import csv


input_json_dir = '../data/all_json/document'
filenames = [f for f in os.listdir(input_json_dir) if os.path.isfile(os.path.join(input_json_dir, f)) and '.DS_Store' not in f]

with open('../data/journal_docid_doi.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for filename in filenames:
        if not filename[0].isdigit():
            file = open(f'{input_json_dir}/{filename}')
            report_id = json.loads(file.read())['report_id']
            doi = filename.split('-')[-1].split('.')[0]
            writer.writerow([report_id, doi])
