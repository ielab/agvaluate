import requests
import json
import time
import spacy
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


def get_dois(articles):
    dois = []
    for article in articles:
        raw_doi = article['identifier']
        doi = raw_doi.replace('doi:', '')
        dois.append(doi)
    return dois


def get_result(issn, apiKeys, start, current_key):
    try:
        response = requests.get(
            f'http://api.springernature.com/meta/v2/json?q=issn:{issn}&p=100&s={start}&api_key={current_key}')
        print(
            f'{response.status_code}: Get Entry -> http://api.springernature.com/meta/v2/json?q=issn:{issn}&p=100&s={start}&api_key={current_key}')
    except:
        current_key = loop_api_keys(current_key, apiKeys)
        print('Exception in Connection, 10 Seconds to Recover')
        time.sleep(10)
        response = requests.get(
            f'http://api.springernature.com/meta/v2/json?q=issn:{issn}&p=100&s={start}&api_key={current_key}')
        print(
            f'{response.status_code}: Get Entry -> http://api.springernature.com/meta/v2/json?q=issn:{issn}&p=100&s={start}&api_key={current_key}')
    while response.status_code != 200:
        time.sleep(5)
        current_key = loop_api_keys(current_key, apiKeys)
        try:
            response = requests.get(
                f'http://api.springernature.com/meta/v2/json?q=issn:{issn}&p=100&s={start}&api_key={current_key}')
            print(
                f'{response.status_code}: Get Entry -> http://api.springernature.com/meta/v2/json?q=issn:{issn}&p=100&s={start}&api_key={current_key}')
        except:
            current_key = loop_api_keys(current_key, apiKeys)
            print('Exception in Connection, 10 Seconds to Recover')
            time.sleep(10)
            response = requests.get(
                f'http://api.springernature.com/meta/v2/json?q=issn:{issn}&p=100&s={start}&api_key={current_key}')
            print(
                f'{response.status_code}: Get Entry -> http://api.springernature.com/meta/v2/json?q=issn:{issn}&p=100&s={start}&api_key={current_key}')
    content = json.loads(response.content)
    return content, current_key


def get_full_text(article):
    pdf_url = None
    html_url = None
    urls = article['url']
    for url in urls:
        if url['format'] == 'pdf':
            pdf_url = url['value']
        elif url['format'] == 'html':
            html_url = url['value']
        else:
            continue

    if pdf_url is not None:
        try:
            full_content = requests.get(pdf_url)
            print(f'{full_content.status_code}: Get Full Text (PDF) -> {pdf_url}')
        except:
            print('Exception in Connection, 10 Seconds to Recover')
            time.sleep(10)
            full_content = requests.get(pdf_url)
            print(f'{full_content.status_code}: Get Full Text (PDF) -> {pdf_url}')
        while full_content.status_code != 200:
            time.sleep(5)
            try:
                full_content = requests.get(pdf_url)
                print(f'{full_content.status_code}: Re-Get Full Text (PDF) -> {pdf_url}')
            except:
                print('Exception in Connection, 10 Seconds to Recover')
                time.sleep(10)
                full_content = requests.get(pdf_url)
                print(f'{full_content.status_code}: Re-Get Full Text (PDF) -> {pdf_url}')
        content = {
            'type': 'pdf',
            'value': full_content
        }
        return content
    elif html_url is not None:
        try:
            full_content = requests.get(html_url)
            print(f'{full_content.status_code}: Get Full Text (HTML) -> {html_url}')
        except:
            print('Exception in Connection, 10 Seconds to Recover')
            time.sleep(10)
            full_content = requests.get(html_url)
            print(f'{full_content.status_code}: Get Full Text (HTML) -> {html_url}')
        while full_content.status_code != 200:
            time.sleep(5)
            try:
                full_content = requests.get(html_url)
                print(f'{full_content.status_code}: Re- Get Full Text (HTML) -> {html_url}')
            except:
                print('Exception in Connection, 10 Seconds to Recover')
                time.sleep(10)
                full_content = requests.get(html_url)
                print(f'{full_content.status_code}: Re- Get Full Text (HTML) -> {html_url}')
        content = {
            'type': 'html',
            'value': full_content
        }
        return content
    else:
        return None


def get_doi_info(doi, apiKeys, current_key):
    try:
        doi_response = requests.get(f'http://api.springernature.com/meta/v2/json?q=doi:{doi}&api_key={current_key}')
        print(f'{doi_response.status_code}: Get DOI Info -> http://api.springernature.com/meta/v2/json?q=doi:{doi}&api_key={current_key}')
    except:
        current_key = loop_api_keys(current_key, apiKeys)
        print('Exception in Connection, 10 Seconds to Recover')
        time.sleep(10)
        doi_response = requests.get(f'http://api.springernature.com/meta/v2/json?q=doi:{doi}&api_key={current_key}')
        print(f'{doi_response.status_code}: Get DOI Info -> http://api.springernature.com/meta/v2/json?q=doi:{doi}&api_key={current_key}')
    while doi_response.status_code != 200:
        time.sleep(5)
        current_key = loop_api_keys(current_key, apiKeys)
        try:
            doi_response = requests.get(f'http://api.springernature.com/meta/v2/json?q=doi:{doi}&api_key={current_key}')
            print(f'{doi_response.status_code}: Re-Get DOI Info -> http://api.springernature.com/meta/v2/json?q=doi:{doi}&api_key={current_key}')
        except:
            current_key = loop_api_keys(current_key, apiKeys)
            print('Exception in Connection, 10 Seconds to Recover')
            time.sleep(10)
            doi_response = requests.get(f'http://api.springernature.com/meta/v2/json?q=doi:{doi}&api_key={current_key}')
            print(f'{doi_response.status_code}: Re-Get DOI Info -> http://api.springernature.com/meta/v2/json?q=doi:{doi}&api_key={current_key}')
    return json.loads(doi_response.content), current_key


def get_article_info(article, journal_name, doi_id):
    pdf_url = 'N/A'
    web_url = 'N/A'
    subjects = []
    keywords = []
    countries = []
    authors = []
    record = article['records'][0]
    facets = article['facets']
    urls = record['url']

    for url in urls:
        if url['format'] == 'pdf':
            pdf_url = url['value']
        elif url['format'] == 'html':
            web_url = url['value']
        else:
            continue

    for facet in facets:
        if facet['name'] == 'subject':
            raw_subjects = facet['values']
            if len(raw_subjects) > 0:
                for raw_subject in raw_subjects:
                    subjects.append(raw_subject['value'])
            else:
                continue
        elif facet['name'] == 'keyword':
            raw_keywords = facet['values']
            if len(raw_keywords) > 0:
                for raw_keyword in raw_keywords:
                    keywords.append(raw_keyword['value'])
            else:
                continue
        elif facet['name'] == 'country':
            raw_countries = facet['values']
            if len(raw_countries) > 0:
                for raw_country in raw_countries:
                    countries.append(raw_country['value'])
            else:
                continue

    raw_authors = record['creators']
    if len(raw_authors) > 0:
        for raw_author in raw_authors:
            authors.append(raw_author['creator'])

    info = {
        'pid': '-',
        'report_id': f'{"_".join(journal_name.lower().split(" "))}-{doi_id}',
        'project_number': f'{"_".join(journal_name.lower().split(" "))}_{doi_id}',
        'report_title': record['title'],
        'region_name': ', '.join(countries) if len(countries) > 0 else 'N/A',
        'category_name': record['publicationName'],
        'research_theme_name': ', '.join(subjects) if len(subjects) > 0 else 'N/A',
        "organisation_name": 'N/A',
        "commence_date": 'N/A',
        "complete_date": record['coverDate'] if 'coverDate' in record.keys() else 'N/A',
        "state": 'N/A',
        "supervisor_name": ', '.join(authors) if len(authors) > 0 else 'N/A',
        "report_type": record['contentType'] if record['contentType'] else 'N/A',
        "report_status": 'Y',
        "publish_date": record['publicationDate'],
        "keywords": ', '.join(keywords) if len(keywords) > 0 else 'N/A',
        "pdf_url": pdf_url,
        "web_url": web_url,
        "passage": ''
    }
    return info


def write_files(info, full_text, full_html_out, pdf_out, article_info_dir):
    full_text_type = full_text['type']

    if full_text_type == 'pdf':
        open(f'{pdf_out}/{info["report_id"]}.pdf', 'wb').write(full_text['value'].content)
    else:
        open(f'{full_html_out}/{info["report_id"]}.txt', 'w+').write(full_text['value'].content.decode('utf-8'))

    with open(f'{article_info_dir}/{info["report_id"]}.json', 'w+') as info_f:
        info_f.write(json.dumps(info))


def loop_api_keys(current_key, apiKeys):
    total_index = len(apiKeys) - 1
    current_index = apiKeys.index(current_key)
    if current_index + 1 > total_index:
        current_index = 0
    return apiKeys[current_index]


def main():
    print("---------------------------------------------------------")
    print("Loading Config...")
    CONFIGFILE = open("../grdc_reports/config.json", "r")
    CONFIG = json.loads(CONFIGFILE.read())
    CONFIGFILE.close()
    print("Loaded.")
    print("---------------------------------------------------------")
    apiKeys = CONFIG['SPRINGER_NATURE_USER_KEY']
    current_key = apiKeys[0]
    journal_names = \
        {
            "Agronomy for Sustainable Development": "1773-0155",
            "Biology and Fertility of Soils": "1432-0789",
            "Irrigation Science": "1432-1319",
            "Journal of Soil Science and Plant Nutrition": "0718-9516",
            "Nutrient Cycling in Agroecosystems": "1573-0867",
            "Plant and Soil": "1573-5036"
        }

    journals = list(journal_names.keys())
    issns = list(journal_names.values())

    for idx, journal_name in enumerate(journals):
        issn = issns[idx]
        print(f'Processing {journal_name}, ISSN: {issn}')
        article_info_dir = f'../../../data/journals/Springer_Nature/{"_".join(journal_name.split(" "))}/article_info'
        pdf_out = f'../../../data/journals/Springer_Nature/{"_".join(journal_name.split(" "))}/pdf'
        full_text_out = f'../../../data/journals/Springer_Nature/{"_".join(journal_name.split(" "))}/text'
        full_json_out = f'../../../data/journals/Springer_Nature/{"_".join(journal_name.split(" "))}/article_info/full_json'
        full_html_out = f'../../../data/journals/Springer_Nature/{"_".join(journal_name.split(" "))}/html'
        passage_json_out = f'../../../data/journals/Springer_Nature/{"_".join(journal_name.split(" "))}/article_info/passage_json'

        if not os.path.exists(article_info_dir):
            os.makedirs(article_info_dir, exist_ok=True)
        if not os.path.exists(pdf_out):
            os.makedirs(pdf_out, exist_ok=True)
        if not os.path.exists(full_json_out):
            os.makedirs(full_json_out, exist_ok=True)
        if not os.path.exists(passage_json_out):
            os.makedirs(passage_json_out, exist_ok=True)
        if not os.path.exists(full_text_out):
            os.makedirs(full_text_out, exist_ok=True)
        if not os.path.exists(full_html_out):
            os.makedirs(full_html_out, exist_ok=True)

        content, current_key = get_result(issn, apiKeys, 1, current_key)
        total_result = int(content['result'][0]['total'])

        for start in range(1, total_result, 100):
            time.sleep(5)
            print('---------------------------------------------------------')
            print(f'Starting Point: {start}/{total_result}')
            print('---------------------------------------------------------')
            content, current_key = get_result(issn, apiKeys, start, current_key)
            articles = content['records']
            dois = get_dois(articles)
            for doi in dois:
                time.sleep(2)
                article, current_key = get_doi_info(doi, apiKeys, current_key)
                doi_id = doi.replace('.', '').replace('-', '').replace('/', '')
                full_text = get_full_text(article['records'][0])
                if full_text is None:
                    continue
                else:
                    info = get_article_info(article, journal_name, doi_id)
                    write_files(info, full_text, full_html_out, pdf_out, article_info_dir)


if __name__ == '__main__':
    main()
