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


def get_articles_in_journal(issn, apiKey, cursor: str = None):
    headers = {
        'Accept': 'application/json',
        'CR-Clickthrough-Client-Token': apiKey,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS)'
    }
    if cursor is None:
        try:
            response = requests.get(f'http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor=*', headers=headers)
            print(f'{response.status_code}: Get Articles -> http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor=*')
        except:
            print('Exception in Connection, 10 Seconds to Recover')
            time.sleep(2)
            response = requests.get(f'http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor=*', headers=headers)
            print(f'{response.status_code}: Get Articles -> http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor=*')
        while response.status_code != 200:
            time.sleep(2)
            try:
                response = requests.get(f'http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor=*', headers=headers)
                print(f'{response.status_code}: Re-Get Articles -> http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor=*')
            except:
                print('Exception in Connection, 10 Seconds to Recover')
                time.sleep(2)
                response = requests.get(f'http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor=*', headers=headers)
                print(f'{response.status_code}: Re-Get Articles -> http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor=*')
        content = json.loads(response.content)
        next_cursor = content['message']['next-cursor']
        articles = content['message']['items']
        print(f'{len(articles)} Journals Found On Page')
        total_results = int(content['message']['total-results'])
    else:
        cursor = cursor.replace('+', '%2B')
        try:
            response = requests.get(f'http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor={cursor}',
                                    headers=headers)
            print(f'{response.status_code}: Get Articles -> http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor={cursor}')
        except:
            print('Exception in Connection, 10 Seconds to Recover')
            time.sleep(2)
            response = requests.get(f'http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor={cursor}',
                                    headers=headers)
            print(f'{response.status_code}: Get Articles -> http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor={cursor}')
        while response.status_code != 200:
            time.sleep(2)
            try:
                requests.get(f'http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor={cursor}', headers=headers)
                print(f'{response.status_code}: Get Articles -> http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor={cursor}')
            except:
                print('Exception in Connection, 10 Seconds to Recover')
                time.sleep(2)
                requests.get(f'http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor={cursor}', headers=headers)
                print(f'{response.status_code}: Get Articles -> http://api.crossref.org/journals/{issn}/works?filter=has-license:true,has-full-text:true&rows=100&cursor={cursor}')
        content = json.loads(response.content)
        next_cursor = content['message']['next-cursor']
        articles = content['message']['items']
        total_results = int(content['message']['total-results'])
    return next_cursor, total_results, articles


def get_full_text(links, apiKey):
    response = None
    for link in links:
        count = 0
        if '/pdf/' in link:
            headers = {
                'Content-Type': 'application/pdf',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS)'
            }
            link = link.replace('/pdf/', '/pdfdirect/')
            link = link.replace('https://', 'https://acsess.')
            cnt = 0
            while True:
                try:
                    time.sleep(2)
                    response = requests.get(link, headers=headers)
                    print(f'{response.status_code}: Get Full Text -> {link}')
                    break
                except:
                    cnt += 1
                    if cnt >= 2:
                        return None
                    print('Exception in Connection, 10 Seconds to Recover')
                    time.sleep(2)
                    continue
            if response.status_code == 200:
                break
            else:
                while response.status_code != 200:
                    cnt = 0
                    while True:
                        try:
                            time.sleep(2)
                            response = requests.get(link, headers=headers)
                            print(f'{response.status_code}: Re-Get Full Text -> {link}')
                            break
                        except:
                            cnt += 1
                            if cnt >= 2:
                                return None
                            print('Exception in Connection, 10 Seconds to Recover')
                            time.sleep(2)
                            continue
                    if response.status_code == 200:
                        break
                    if response.status_code == 403:
                        return None
                    if response.status_code == 500 or response.status_code == 404:
                        time.sleep(2)
                        count += 1
                    if count >= 2:
                        return None
                if response.status_code == 200:
                    break
                if response.status_code == 403:
                    continue
        else:
            # continue
            headers = {
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS)',
                'CR-Clickthrough-Client-Token': apiKey
            }
            cnt = 0
            while True:
                try:
                    time.sleep(2)
                    response = requests.get(link, headers=headers)
                    print(f'{response.status_code}: Get Full Text -> {link}')
                    break
                except:
                    cnt += 1
                    if cnt >= 2:
                        return None
                    print('Exception in Connection, 10 Seconds to Recover')
                    time.sleep(2)
                    continue
            if response.status_code == 200:
                break
            else:
                while response.status_code != 200:
                    cnt = 0
                    while True:
                        try:
                            time.sleep(2)
                            response = requests.get(link, headers=headers)
                            print(f'{response.status_code}: Re-Get Full Text -> {link}')
                            break
                        except:
                            cnt += 1
                            if cnt >= 2:
                                return None
                            print('Exception in Connection, 10 Seconds to Recover')
                            time.sleep(2)
                            continue
                    if response.status_code == 200:
                        break
                    if response.status_code == 403:
                        break
                    if response.status_code == 500 or response.status_code == 404:
                        time.sleep(2)
                        count += 1
                    if count >= 2:
                        break
                if response.status_code == 200:
                    break
                if response.status_code == 403:
                    continue
    return response


def get_affiliations(raw_affiliations):
    affiliations = []
    if isinstance(raw_affiliations, list):
        for raw_affiliation in raw_affiliations:
            if raw_affiliation['name'] not in affiliations:
                affiliations.append(raw_affiliation['name'])
    else:
        affiliations.append(raw_affiliations['name'])
    return ', '.join(affiliations)


def get_article_info(journal_name, article, doi_id, link):
    authors = []
    affiliations = []
    if 'author' in article.keys():
        raw_authors_and_affils = article['author']
        if isinstance(raw_authors_and_affils, list):
            for raw_authors_and_affil in raw_authors_and_affils:
                given = raw_authors_and_affil['given'] if 'given' in raw_authors_and_affil.keys() else None
                family = raw_authors_and_affil['family'] if 'family' in raw_authors_and_affil.keys() else None
                if given and family:
                    authors.append(given + family)
                if 'affiliation' in raw_authors_and_affil.keys():
                    affiliation = get_affiliations(raw_authors_and_affil['affiliation'])
                    affiliations.append(affiliation)
        else:
            given = raw_authors_and_affils['given'] if 'given' in raw_authors_and_affils.keys() else None
            family = raw_authors_and_affils['family'] if 'family' in raw_authors_and_affils.keys() else None
            if given and family:
                    authors.append(given + family)
            if 'affiliation' in raw_authors_and_affils.keys():
                affiliation = get_affiliations(raw_authors_and_affils['affiliation'])
                affiliations.append(affiliation)

    if 'published-online' in article.keys() and article['published-online']:
        date_parts = [str(d) for d in article['published-online']['date-parts'][0]]
        publish_date = '-'.join(date_parts)
    elif 'published-print' in article.keys() and article['published-print']:
        date_parts = [str(d) for d in article['published-print']['date-parts'][0]]
        publish_date = '-'.join(date_parts)
    else:
        publish_date = 'N/A'
    
    if 'title' in article.keys():
        if article['title']:
            title = article['title'][0]
        else:
            title = 'N/A'
    else:
        title = 'N/A'

    info = {
        'pid': '-',
        'report_id': f'{"_".join(journal_name.lower().split(" "))}-{doi_id}',
        'project_number': f'{"_".join(journal_name.lower().split(" "))}-{doi_id}',
        'report_title': title,
        'region_name': 'N/A',
        'category_name': article['container-title'][0] if article['container-title'] else 'N/A',
        'research_theme_name': ','.join(article['subject']) if 'subject' in article.keys() and article['subject'] else 'N/A',
        "organisation_name": '; '.join(affiliations) if len(affiliations) > 0 else 'N/A',
        "commence_date": 'N/A',
        "complete_date": 'N/A',
        "state": 'N/A',
        "supervisor_name": ', '.join(authors) if len(authors) > 0 else 'N/A',
        "report_type": article['type'] if article['type'] else 'N/A',
        "report_status": 'Y',
        "publish_date": publish_date,
        "keywords": 'N/A',
        "pdf_url": '; '.join(link),
        "web_url": article['URL'] if article['URL'] else 'N/A',
        "passage": ''
    }
    return info


def write_files(info, full_text_stream, pdf_out, article_info_dir):
    open(f'{pdf_out}/{info["report_id"]}.pdf', 'wb').write(full_text_stream.content)
    with open(f'{article_info_dir}/{info["report_id"]}.json', 'w+') as aij_out:
        aij_out.write(json.dumps(info))


def main():
    print("---------------------------------------------------------")
    print("Loading Config...")
    CONFIGFILE = open("../config.json", "r")
    CONFIG = json.loads(CONFIGFILE.read())
    CONFIGFILE.close()
    print("Loaded.")
    print("---------------------------------------------------------")
    apiKey = CONFIG['WILEY_API_KEY']
    journal_names = \
        {
            "Agronomy Journal": "1435-0645",
            "Crop Science": "1435-0653",
            "European Journal of Soil Science": "1365-2389",
            "Global Change Biology": "1365-2486",
            "Journal of Agronomy and Crop Science": "1439-037X",
            "Journal of Plant Nutrition and Soil Science": "1522-2624",
            "Land Degradation and Development": "1099-145X",
            "Soil Science Society of America Journal": "1435-0661",
            "Soil Use and Management": "1475-2743",
            "The Journal of the Science of Food and Agriculture": "1097-0010"
        }

    journals = list(journal_names.keys())
    issns = list(journal_names.values())

    for idx, journal_name in enumerate(journals):
        issn = issns[idx]
        print(f'Processing {journal_name}, ISSN: {issn}')
        article_info_dir = f'/Users/hangli/ielab/AgAsk/code/GRDC_Reports/journals/Wiley/{"_".join(journal_name.split(" "))}/article_info'
        pdf_out = f'/Users/hangli/ielab/AgAsk/code/GRDC_Reports/journals/Wiley/{"_".join(journal_name.split(" "))}/pdf'
        full_text_out = f'/Users/hangli/ielab/AgAsk/code/GRDC_Reports/journals/Wiley/{"_".join(journal_name.split(" "))}/text'
        full_json_out = f'/Users/hangli/ielab/AgAsk/code/GRDC_Reports/journals/Wiley/{"_".join(journal_name.split(" "))}/article_info/full_json'
        passage_json_out = f'/Users/hangli/ielab/AgAsk/code/GRDC_Reports/journals/Wiley/{"_".join(journal_name.split(" "))}/article_info/passage_json'

        if not os.path.exists(article_info_dir):
            os.mkdir(article_info_dir)
        if not os.path.exists(pdf_out):
            os.mkdir(pdf_out)
        if not os.path.exists(full_json_out):
            os.mkdir(full_json_out)
        if not os.path.exists(passage_json_out):
            os.mkdir(passage_json_out)
        if not os.path.exists(full_text_out):
            os.mkdir(full_text_out)

        first_page = True

        next_cursor, total_results, _ = get_articles_in_journal(issn, apiKey, None)

        # next_cursor = ''

        while next_cursor is not None and next_cursor != '':
            time.sleep(1)
            print('---------------------------------------------------------')
            print(f'Total: {total_results}')
            print('---------------------------------------------------------')
            if first_page:
                next_cursor, _, articles = get_articles_in_journal(issn, apiKey, None)
                first_page = False
            else:
                next_cursor, _, articles = get_articles_in_journal(issn, apiKey, next_cursor)
            if len(articles) == 0:
                break
            for article in articles:
                time.sleep(1)
                doi = article['DOI']
                doi_id = doi.replace('/', '').replace('.', '')
                print(f'DOI: {doi}')
                links = article['link']
                link = []
                if isinstance(links, list):
                    for raw_link in links:
                        if raw_link['content-type'] == 'application/pdf' or raw_link['intended-application'] == 'text-mining':
                            link.append(raw_link['URL'])
                else:
                    raw_link = article['link']
                    if raw_link['content-type'] == 'application/pdf' or raw_link['intended-application'] == 'text-mining':
                        link = raw_link['URL']
                if len(link) == 0:
                    print(f'No Full Text Found For {doi}')
                    continue
                else:
                    print(f'Full Text Link: {link}')
                    full_text_stream = get_full_text(link, apiKey)
                    if full_text_stream is None:
                        print(f'No Full Text Found For {doi}')
                        continue
                    else:
                        info = get_article_info(journal_name, article, doi_id, link)
                        write_files(info, full_text_stream, pdf_out, article_info_dir)


if __name__ == '__main__':
    main()
