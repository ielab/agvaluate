import requests
import json
import time
import spacy
import math
import os

nlp = spacy.blank("en")
nlp.add_pipe(nlp.create_pipe("sentencizer"))

"""
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
}
"""


def get_entries(page_number, query, apiKey):
    try:
        response = requests.get(
            f'https://api.elsevier.com/content/search/sciencedirect?start={page_number}&count=100&query={query}&apiKey={apiKey}')
        print(f'{response.status_code}: Get Entry -> https://api.elsevier.com/content/search/sciencedirect?start={page_number}&count=100&query={query}&apiKey={apiKey}')
    except:
        print('Exception in Connection, 10 Seconds to Recover')
        time.sleep(10)
        response = requests.get(
            f'https://api.elsevier.com/content/search/sciencedirect?start={page_number}&count=100&query={query}&apiKey={apiKey}')
        print(f'{response.status_code}: Get Entry -> https://api.elsevier.com/content/search/sciencedirect?start={page_number}&count=100&query={query}&apiKey={apiKey}')
    while response.status_code != 200:
        time.sleep(5)
        try:
            response = requests.get(
                f'https://api.elsevier.com/content/search/sciencedirect?start={page_number}&count=100&query={query}&apiKey={apiKey}')
            print(
                f'{response.status_code}: Re-Get Entry -> https://api.elsevier.com/content/search/sciencedirect?start={page_number}&count=100&query={query}&apiKey={apiKey}')
        except:
            print('Exception in Connection, 10 Seconds to Recover')
            time.sleep(10)
            response = requests.get(
                f'https://api.elsevier.com/content/search/sciencedirect?start={page_number}&count=100&query={query}&apiKey={apiKey}')
            print(
                f'{response.status_code}: Re-Get Entry -> https://api.elsevier.com/content/search/sciencedirect?start={page_number}&count=100&query={query}&apiKey={apiKey}')
    content = json.loads(response.content)
    return content, response.status_code


def get_info(pii, apiKey):
    headers = {
        'Accept': 'application/json',
    }
    try:
        response = requests.get(
            f'https://api.elsevier.com/content/abstract/pii/{pii}?apiKey={apiKey}', headers=headers)
        print(
            f'{response.status_code}: Get Abstract -> https://api.elsevier.com/content/abstract/pii/{pii}?apiKey={apiKey}')
    except:
        print('Exception in Connection, 10 Seconds to Recover')
        time.sleep(10)
        response = requests.get(
            f'https://api.elsevier.com/content/abstract/pii/{pii}?apiKey={apiKey}', headers=headers)
        print(
            f'{response.status_code}: Get Abstract -> https://api.elsevier.com/content/abstract/pii/{pii}?apiKey={apiKey}')
    while response.status_code != 200:
        time.sleep(5)
        try:
            response = requests.get(
                f'https://api.elsevier.com/content/abstract/pii/{pii}?apiKey={apiKey}',
                headers=headers)
            print(
                f'{response.status_code}: Re-Get Abstract -> https://api.elsevier.com/content/abstract/pii/{pii}?apiKey={apiKey}')
        except:
            print('Exception in Connection, 10 Seconds to Recover')
            time.sleep(10)
            response = requests.get(
                f'https://api.elsevier.com/content/abstract/pii/{pii}?apiKey={apiKey}',
                headers=headers)
            print(
                f'{response.status_code}: Re-Get Abstract -> https://api.elsevier.com/content/abstract/pii/{pii}?apiKey={apiKey}')
        if response.status_code == 404:
            return None
    content = json.loads(response.content)
    subject_areas = []
    raw_subject_areas = content['abstracts-retrieval-response']['subject-areas']['subject-area']
    for area in raw_subject_areas:
        subject_areas.append(list(area.values())[1])
    year_created = content['abstracts-retrieval-response']['item']['bibrecord']['item-info']['history']['date-created'][
        '@year']
    month_created = content['abstracts-retrieval-response']['item']['bibrecord']['item-info']['history']['date-created']['@month']
    day_created = content['abstracts-retrieval-response']['item']['bibrecord']['item-info']['history']['date-created'][
        '@day']
    year_sort = content['abstracts-retrieval-response']['item']['ait:process-info']['ait:date-sort']['@year']
    month_sort = content['abstracts-retrieval-response']['item']['ait:process-info']['ait:date-sort']['@month']
    day_sort = content['abstracts-retrieval-response']['item']['ait:process-info']['ait:date-sort']['@day']
    keywords = []
    raw_keywords = content['abstracts-retrieval-response']['authkeywords']
    if raw_keywords is None:
        keywords = ['N/A']
    else:
        if isinstance(raw_keywords['author-keyword'], list):
            for keyword in raw_keywords['author-keyword']:
                keywords.append(list(keyword.values())[1])
        else:
            keywords.append(list(raw_keywords['author-keyword'].values())[1])
    countries = []
    organizations = []
    raw_country = content['abstracts-retrieval-response']['item']['bibrecord']['head']['author-group']
    if isinstance(raw_country, list):
        for item in raw_country:
            if 'country' in item['affiliation'].keys():
                if item['affiliation']['country'] not in countries:
                    countries.append(item['affiliation']['country'])
                if 'organizations' in item['affiliation'].keys():
                    raw_orgs = item['affiliation']['organization']
                    if isinstance(raw_orgs, list):
                        temp_org = []
                        for org in raw_orgs:
                            temp_org.append(list(org.values())[0])
                        organizations.append(', '.join(temp_org))
                    else:
                        organizations.append(list(raw_orgs.values())[0])
    else:
        if 'affiliation' in raw_country.keys():
            countries.append(
                content['abstracts-retrieval-response']['item']['bibrecord']['head']['author-group']['affiliation'][
                    'country'])
            if 'organization' in content['abstracts-retrieval-response']['item']['bibrecord']['head']['author-group']['affiliation'].keys():
                raw_orgs = content['abstracts-retrieval-response']['item']['bibrecord']['head']['author-group']['affiliation']['organization']
                if isinstance(raw_orgs, list):
                    temp_org = []
                    for org in raw_orgs:
                        temp_org.append(list(org.values())[0])
                    organizations.append(', '.join(temp_org))
                else:
                    organizations.append(list(raw_orgs.values())[0])
    if len(countries) == 1:
        country = countries[0]
    else:
        country = ', '.join(countries)
    if len(organizations) == 1:
        organization = organizations[0]
    else:
        organization = ' '.join(organizations)
    info = {
        'country': country if country != '' else 'N/A',
        'subject-area': ', '.join(subject_areas),
        'organization': organization if organization != '' else 'N/A',
        'date-created': f'{year_created}-{month_created}-{day_created}',
        'date-sort': f'{year_sort}-{month_sort}-{day_sort}',
        'keywords': ','.join(keywords),
        'type': content['abstracts-retrieval-response']['coredata']['prism:aggregationType']
    }
    return info


def get_full_text(pii, apiKey):
    headers = {
        'Accept': 'application/json',
    }
    try:
        response = requests.get(
            f'https://api.elsevier.com/content/article/pii/{pii}?apiKey={apiKey}', headers=headers)
        print(f'{response.status_code}: Get Full Text -> https://api.elsevier.com/content/article/pii/{pii}?apiKey={apiKey}')
    except:
        print('Exception in Connection, 10 Seconds to Recover')
        time.sleep(10)
        response = requests.get(
            f'https://api.elsevier.com/content/article/pii/{pii}?apiKey={apiKey}', headers=headers)
        print(f'{response.status_code}: Get Full Text -> https://api.elsevier.com/content/article/pii/{pii}?apiKey={apiKey}')
    while response.status_code != 200:
        time.sleep(5)
        try:
            response = requests.get(
                f'https://api.elsevier.com/content/article/pii/{pii}?apiKey={apiKey}',
                headers=headers)
            print(f'{response.status_code}: Re-Get Full Text -> https://api.elsevier.com/content/article/pii/{pii}?apiKey={apiKey}')
        except:
            print('Exception in Connection, 10 Seconds to Recover')
            time.sleep(10)
            response = requests.get(
                f'https://api.elsevier.com/content/article/pii/{pii}?apiKey={apiKey}',
                headers=headers)
            print(f'{response.status_code}: Re-Get Full Text -> https://api.elsevier.com/content/article/pii/{pii}?apiKey={apiKey}')
    content = json.loads(response.content)
    full_text = content['full-text-retrieval-response']['originalText']
    if isinstance(full_text, dict):
        return None
    return full_text


def get_article_info(entry, journal_name, apiKey):
    authors = []
    if entry['authors'] is None:
        return None, None
    raw_authors = entry['authors']['author']
    if isinstance(raw_authors, list):
        for author in raw_authors:
            authors.append(list(author.values())[0])
    else:
        authors.append(raw_authors)
    additional_info = get_info(entry['pii'], apiKey)
    full_text = get_full_text(entry['pii'], apiKey)
    if full_text is None:
        return None, None
    if additional_info is None:
        info = {
            'pid': '-',
            'report_id': f'{"_".join(journal_name.lower().split(" "))}-{entry["pii"]}',
            'project_number': f'{"_".join(journal_name.lower().split(" "))}-{entry["pii"]}',
            'report_title': entry['dc:title'],
            'region_name': 'N/A',
            'category_name': entry['prism:publicationName'],
            'research_theme_name': 'N/A',
            "organisation_name": 'N/A',
            "commence_date": 'N/A',
            "complete_date": 'N/A',
            "state": 'N/A',
            "supervisor_name": ', '.join(authors),
            "report_type": 'N/A',
            "report_status": 'Y',
            "publish_date": entry['prism:coverDate'],
            "keywords": 'N/A',
            "pdf_url": entry['prism:url'],
            "web_url": entry['prism:url'],
            "passage": ''
        }
    else:
        info = {
            'pid': '-',
            'report_id': f'{"_".join(journal_name.lower().split(" "))}-{entry["pii"]}',
            'project_number': f'{"_".join(journal_name.lower().split(" "))}-{entry["pii"]}',
            'report_title': entry['dc:title'],
            'region_name': additional_info['country'],
            'category_name': entry['prism:publicationName'],
            'research_theme_name': additional_info['subject-area'],
            "organisation_name": additional_info['organization'],
            "commence_date": additional_info['date-created'],
            "complete_date": additional_info['date-sort'],
            "state": 'N/A',
            "supervisor_name": ', '.join(authors),
            "report_type": additional_info['type'],
            "report_status": 'Y',
            "publish_date": entry['prism:coverDate'],
            "keywords": additional_info['keywords'],
            "pdf_url": entry['prism:url'],
            "web_url": entry['prism:url'],
            "passage": ''
        }
    return info, full_text


def split_and_write_files(info, full_text, full_text_out, full_json_out, passage_json_out, article_info_dir):
    passages = []
    doc = nlp(full_text)
    full_info = info
    article_info = info
    sentences = [sent.string.strip() for sent in doc.sents]
    chunks = list(chunk(sentences, 2))
    for c in chunks:
        passages.append(' '.join(c))
    for ind, passage in enumerate(passages):
        info['passage'] = passage
        info['pid'] = f'{info["report_id"]}-{ind + 1}'
        with open(f'{passage_json_out}/{info["report_id"]}-{ind + 1}.json', 'w+') as p_out:
            p_out.write(json.dumps(info))
    with open(f'{full_text_out}/{info["report_id"]}.txt', 'w+') as ft_out:
        ft_out.write(full_text)
    full_info['passage'] = full_text
    full_info['pid'] = '-'
    with open(f'{full_json_out}/{info["report_id"]}.json', 'w+') as fj_out:
        fj_out.write(json.dumps(full_info))
    article_info['pid'] = '-'
    article_info['passage'] = ''
    with open(f'{article_info_dir}/{info["report_id"]}.json', 'w+') as aij_out:
        aij_out.write(json.dumps(article_info))


def chunk(sentences, chunk_size):
    for i in range(0, len(sentences), chunk_size):
        yield sentences[i:i + chunk_size]


def main():
    print("---------------------------------------------------------")
    print("Loading Config...")
    CONFIGFILE = open("../config.json", "r")
    CONFIG = json.loads(CONFIGFILE.read())
    CONFIGFILE.close()
    print("Loaded.")
    print("---------------------------------------------------------")
    apiKey = CONFIG['ELSEVIER_API_KEY'][0]
    journal_names = \
        [
            'Advances in Agronomy', 'Agricultural Systems', 'Agricultural Water Management',
            'Agriculture Ecosystems and Environment',
            'Catena', 'European Journal of Agronomy', 'Field Crops Research', 'Geoderma',
            'Global Food Security', 'Soil and Tillage Research', 'Soil Biology and Biochemistry'
        ]
    for journal_name in journal_names:
        print(f'Processing {journal_name}')
        bq_name = '+'.join(journal_name.split(' '))
        article_info_dir = f'/Users/hangli/ielab/AgAsk/code/GRDC_Reports/journals/Elsevier/{"_".join(journal_name.split(" "))}/article_info'
        full_text_out = f'/Users/hangli/ielab/AgAsk/code/GRDC_Reports/journals/Elsevier/{"_".join(journal_name.split(" "))}/text'
        full_json_out = f'/Users/hangli/ielab/AgAsk/code/GRDC_Reports/journals/Elsevier/{"_".join(journal_name.split(" "))}/article_info/full_json'
        passage_json_out = f'/Users/hangli/ielab/AgAsk/code/GRDC_Reports/journals/Elsevier/{"_".join(journal_name.split(" "))}/article_info/passage_json'
        pdf_out = f'/Users/hangli/ielab/AgAsk/code/GRDC_Reports/journals/Elsevier/{"_".join(journal_name.split(" "))}/pdf'

        if not os.path.exists(article_info_dir):
            os.mkdir(article_info_dir)
        if not os.path.exists(full_text_out):
            os.mkdir(full_text_out)
        if not os.path.exists(full_json_out):
            os.mkdir(full_json_out)
        if not os.path.exists(passage_json_out):
            os.mkdir(passage_json_out)
        if not os.path.exists(pdf_out):
            os.mkdir(pdf_out)

        query = 'all({})+AND+srctitle({})'.format(bq_name, bq_name)

        content, status = get_entries(0, query, apiKey)
        print(f'{status}: Get Total Results')

        total_result = content['search-results']['opensearch:totalResults']
        print(f'Total Results: {total_result}')
        pages = math.ceil(int(total_result) / 100)
        print(f'Total Pages: {pages}')

        for i in range(0, pages):
            time.sleep(5)
            print(f'Page Number: {i + 1}/{pages}')
            content, status = get_entries(i, query, apiKey)
            print(f'Entry: {status}')
            while status != 200:
                time.sleep(2)
                content, status = get_entries(i, query, apiKey)
                print(f'Re-Entry: {status}')
            entries = content['search-results']['entry']
            for entry in entries:
                time.sleep(5)
                print(f'PII: {entry["pii"]}')
                info, full_text = get_article_info(entry, journal_name, apiKey)
                if info is None:
                    continue
                else:
                    split_and_write_files(info, full_text, full_text_out, full_json_out, passage_json_out, article_info_dir)


if __name__ == '__main__':
    main()
