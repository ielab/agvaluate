import requests
from bs4 import BeautifulSoup
import time
import random
import json

random.seed(10)
url = 'https://www.mdpi.com/search?q=&journal=agronomy&sort=pubdate&page_count=10&page_no={}'
pdf_url_prefix = 'https://www.mdpi.com'


def main():
    for page in range(1, 340):
        time.sleep(5)
        titles = []
        authors = []
        web_urls = []
        pdf_urls = []
        abstracts = []
        ids = []
        keywords = []
        organizations = []
        commence_dates = []
        complete_dates = []
        publish_dates = []
        research_theme_names = []
        formatted_url = url.format(page)
        try:
            response = make_request(formatted_url)
            print(f'{response.status_code}: {formatted_url}')
        except:
            print('Exception in Connection, 10 Seconds to Recover')
            time.sleep(10)
            response = make_request(formatted_url)
            print(f'{response.status_code}: {formatted_url}')
        while response.status_code != 200:
            try:
                print(f'{response.status_code}: {formatted_url}')
                response = make_request(formatted_url)
            except:
                print('Exception in Connection, 10 Seconds to Recover')
                time.sleep(10)
                print(f'{response.status_code}: {formatted_url}')
                response = make_request(formatted_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        raw_title_links = soup.findAll("a", {"class": "title-link"})
        for link in raw_title_links:
            titles.append(link.text.strip())
        raw_authors = soup.findAll("div", {"class": "authors"})
        for raw_author in raw_authors:
            authors.append(raw_author.text.replace('\n', '').replace('by', ''))
        raw_pdf_links = soup.findAll("a", {"class", "UD_Listings_ArticlePDF"})
        for raw_pdf_link in raw_pdf_links:
            pdf_urls.append(f'{pdf_url_prefix}{raw_pdf_link["href"]}')
            weburl = f'{pdf_url_prefix}{raw_pdf_link["href"][0:len(raw_pdf_link["href"])-4]}'
            web_urls.append(weburl)
            try:
                inner_response = make_request(weburl)
                print(f'{inner_response.status_code}: {weburl}')
            except:
                print('Exception in Connection, 10 Seconds to Recover')
                time.sleep(10)
                inner_response = make_request(weburl)
                print(f'{inner_response.status_code}: {weburl}')
            while inner_response.status_code != 200:
                try:
                    print(f'{inner_response.status_code}: {weburl}')
                    inner_response = make_request(weburl)
                except:
                    print('Exception in Connection, 10 Seconds to Recover')
                    time.sleep(10)
                    print(f'{inner_response.status_code}: {weburl}')
                    inner_response = make_request(weburl)
            inner_soup = BeautifulSoup(inner_response.content, 'html.parser')
            raw_organizations = inner_soup.findAll("div", {"class": "art-affiliations"})
            if raw_organizations is not None:
                for raw_organization in raw_organizations:
                    organizations.append(raw_organization.text.strip().replace('\n', ' '))
            else:
                organizations.append('N/A')
            raw_pub_histo = inner_soup.find("div", {"class": "pubhistory"})
            if raw_pub_histo is not None:
                dates = raw_pub_histo.text.strip().split(' / ')
                if len(dates) == 4:
                    commence_dates.append(dates[0].split(': ')[1])
                    complete_dates.append(dates[2].split(': ')[1])
                    publish_dates.append(dates[3].split(': ')[1])
                elif len(dates) == 3:
                    commence_dates.append(dates[0].split(': ')[1])
                    complete_dates.append(dates[1].split(': ')[1])
                    publish_dates.append(dates[2].split(': ')[1])
                else:
                    commence_dates.append('N/A')
                    complete_dates.append('N/A')
                    publish_dates.append('N/A')
            else:
                commence_dates.append('N/A')
                complete_dates.append('N/A')
                publish_dates.append('N/A')
            raw_keyword = inner_soup.find("div", {"class": "art-keywords in-tab hypothesis_container"})
            if raw_keyword is not None:
                keyword = ','.join(raw_keyword.text.strip().split('\n')[1].split('; '))
                keywords.append(keyword)
            else:
                keywords.append('N/A')
            raw_theme = inner_soup.find("div", {"class": "belongsTo"})
            if raw_theme is not None:
                a_link = raw_theme.findChildren("a", recursive=False)
                for a in a_link:
                    research_theme_names.append(a.text)
            else:
                research_theme_names.append('N/A')
            raw_abstract_full = inner_soup.find("div", {"class": "art-abstract in-tab hypothesis_container"})
            abstracts.append(raw_abstract_full.text.strip().replace('\n', '').replace('View Full-Text', ''))
        raw_web_link_dates = soup.findAll("div", {"class": "color-grey-dark"})
        for raw_web_link_date in raw_web_link_dates:
            raw_link_date = raw_web_link_date.text.replace('\n', '')
            parts = raw_link_date.split(' - ')
            pre_parts = parts[0].split('; ')
            part = pre_parts[1]
            if ' ' in part:
                part = part.split(' ')[0]
            ids.append(part.split('/')[-1].split('y')[1])
        for ind, did in enumerate(ids):
            with open(f'/Users/hangli/ielab/AgAsk/code/GRDC_Reports/journals/Agronomy/article_info/agronomy-{did}.json', 'w+') as fout:
                info = {
                    "pid": "-",
                    "report_id": f'agronomy-{did}',
                    "project_number": f'agronomy-{did}',
                    "report_title": titles[ind],
                    "region_name": "N/A",
                    "category_name": "Agronomy",
                    "research_theme_name": research_theme_names[ind],
                    "organisation_name": organizations[ind],
                    "commence_date": commence_dates[ind],
                    "complete_date": complete_dates[ind],
                    "state": "N/A",
                    "supervisor_name": authors[ind],
                    "report_type": "Journal Article",
                    "report_status": "Y",
                    "publish_date": publish_dates[ind],
                    "keywords": keywords[ind],
                    "pdf_url": pdf_urls[ind],
                    "web_url": web_urls[ind],
                    "passage": abstracts[ind]
                }
                fout.write(json.dumps(info))
            print(f'Downloading: {pdf_urls[ind]}')
            try:
                pdf_file = make_request(pdf_urls[ind])
            except:
                print('Exception in Connection, 10 Seconds to Recover')
                time.sleep(10)
                pdf_file = make_request(pdf_urls[ind])
            open(f'/Users/hangli/ielab/AgAsk/code/GRDC_Reports/journals/Agronomy/pdf/agronomy-{did}.pdf', 'wb').write(pdf_file.content)


def make_request(url):
    time.sleep(random.randint(1, 4))
    return requests.get(url)


if __name__ == "__main__":
    main()
