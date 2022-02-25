import os
import json
import spacy
from tqdm import tqdm

nlp = spacy.blank("en")
nlp.add_pipe(nlp.create_pipe("sentencizer"))


def run():
    path_prefix = 'json_cleaned_no_split/{}'
    output_path_prefix = 'json_passages/{}'
    filenames = os.listdir('json_cleaned_no_split')
    for filename in tqdm(filenames, desc='Processing File', total=len(filenames)):
        if not filename.startswith('.'):
            fin = open(path_prefix.format(filename), 'r')
            report_json = json.loads(fin.read())
            reformat_json_report(report_json, output_path_prefix)


def reformat_json_report(input_json, output_path_prefix):
    report_id = input_json['report_id'] if input_json['report_id'] is not None else ''
    project_number = f'grdc-{input_json["project_number"]}' if input_json['project_number'] is not None else ''
    report_title = input_json['report_title'] if input_json['report_title'] is not None else ''
    region_name = input_json['region_name'] if input_json['region_name'] is not None else ''
    category_name = input_json['category_name'] if input_json['category_name'] is not None else ''
    research_theme_name = input_json['research_theme_name'] if input_json['research_theme_name'] is not None else ''
    organisation_name = input_json['organisation_name'] if input_json['organisation_name'] is not None else ''
    commence_date = input_json['commence_date'] if input_json['commence_date'] is not None else ''
    complete_date = input_json['complete_date'] if input_json['complete_date'] is not None else ''
    state = input_json['state'] if input_json['state'] is not None else ''
    supervisor_name = input_json['supervisor_name'] if input_json['supervisor_name'] is not None else ''
    report_type = input_json['report_type'] if input_json['report_type'] is not None else ''
    report_status = input_json['report_status'] if input_json['report_status'] is not None else ''
    publish_date = input_json['publish_date'] if input_json['publish_date'] is not None else ''
    report_summary = input_json['report_summary'] if input_json['report_summary'] is not None else ''
    keywords = input_json['keywords'] if input_json['keywords'] is not None else ''
    pdf_url = input_json['pdf_url'] if input_json['pdf_url'] is not None else ''
    web_url = input_json['web_url'] if input_json['web_url'] is not None else ''
    html_content = input_json['html_content'] if input_json['html_content'] is not None else ''
    report_achievement = input_json['report_achievement'] if input_json['report_achievement'] is not None else ''
    report_conclusion = input_json['report_conclusion'] if input_json['report_conclusion'] is not None else ''
    report_outcome = input_json['report_outcome'] if input_json['report_outcome'] is not None else ''
    report_recommendation = input_json['report_recommendation'] if input_json[
                                                                       'report_recommendation'] is not None else ''
    report_discussion = input_json['report_discussion'] if input_json['report_discussion'] is not None else ''
    other_research = input_json['other_research'] if input_json['other_research'] is not None else ''
    ip_summary = input_json['ip_summary'] if input_json['ip_summary'] is not None else ''
    additional_information = input_json['additional_information'] if input_json[
                                                                         'additional_information'] is not None else ''
    report_full_text_content = input_json['report_full_text_content'] if input_json[
                                                                             'report_full_text_content'] is not None else ''

    doc_passages = split_document_into_passage(
        f'{report_summary} {html_content} {report_achievement} {report_conclusion} {report_outcome} {report_recommendation} {report_discussion} {other_research} {ip_summary} {additional_information} {report_full_text_content}')
    for ind, p in enumerate(doc_passages):
        new_report_json = {
            'pid': f'grdc-{report_id}-{ind + 1}',
            'report_id': f'grdc-{report_id}',
            'project_number': project_number,
            'report_title': report_title,
            'region_name': region_name,
            'category_name': category_name,
            'research_theme_name': research_theme_name,
            'organisation_name': organisation_name,
            'commence_date': commence_date,
            'complete_date': complete_date,
            'state': state,
            'supervisor_name': supervisor_name,
            'report_type': report_type,
            'report_status': report_status,
            'publish_date': publish_date,
            'keywords': keywords,
            'pdf_url': pdf_url,
            'web_url': web_url,
            'passage': p[:32700]  # Because Anserini cannot handle input larger than 32766
        }

        write_file(new_report_json, output_path_prefix, f'grdc-{report_id}-{ind + 1}.json')

    attachments = input_json['attachments']

    if len(attachments) != 0:
        for attachment in attachments:
            attachment_full_text_content = attachment['attachment_full_text_content'] if attachment[
                                                                                             'attachment_full_text_content'] is not None else ''
            attachment_url = attachment['attachment_url'] if attachment['attachment_url'] is not None else ''
            attachment_id = attachment['attachment_id'] if attachment['attachment_id'] is not None else ''
            attachment_name = attachment['attachment_name'] if attachment['attachment_name'] is not None else ''
            attachment_type = attachment['attachment_type'] if attachment['attachment_type'] is not None else ''
            if attachment_full_text_content != '':
                att_passages = split_document_into_passage(attachment_full_text_content)
                for ind, p in enumerate(att_passages):
                    new_attachment_json = {
                        'pid': f'grdc-{report_id}-{attachment_id}-{ind + 1}',
                        'report_id': f'grdc-{attachment_id}',
                        'project_number': project_number,
                        'report_title': attachment_name,
                        'region_name': region_name,
                        'category_name': category_name,
                        'research_theme_name': research_theme_name,
                        'organisation_name': organisation_name,
                        'commence_date': commence_date,
                        'complete_date': complete_date,
                        'state': state,
                        'supervisor_name': supervisor_name,
                        'report_type': attachment_type,
                        'report_status': report_status,
                        'publish_date': publish_date,
                        'keywords': keywords,
                        'pdf_url': attachment_url,
                        'web_url': attachment_url,
                        'passage': p[:32700]  # Because Anserini cannot handle input larger than 32766
                    }

                    write_file(new_attachment_json, output_path_prefix, f'grdc-{report_id}-{attachment_id}-{ind + 1}.json')


def split_document_into_passage(document):
    passages = []
    doc = nlp(document)
    sentences = [sent.string.strip() for sent in doc.sents]
    chunks = list(chunk(sentences, 2))
    for c in chunks:
        passages.append(' '.join(c))
    return passages


def chunk(sentences, chunk_size):
    for i in range(0, len(sentences), chunk_size):
        yield sentences[i:i + chunk_size]


def write_file(new_report_json, output_dir, filename):
    fout = open(output_dir.format(filename), 'a+')
    fout.write(json.dumps(new_report_json))
    fout.close()


if __name__ == '__main__':
    run()
