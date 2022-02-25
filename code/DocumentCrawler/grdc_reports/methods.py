import requests
import json
import os
import wget
import time
from tika import parser
from bs4 import BeautifulSoup


# Get available reports as a list from the API
# Input:
# CONFIG -> loaded config data
# Output:
# reportList -> json data containing all reports information
def getReportList(CONFIG):
    response = requests.get(CONFIG["GET_REPORT_LIST"])
    if response.status_code == 200:
        reportList = json.loads(response.content)
        return reportList
    else:
        return None


# Get report web content as web.txt, pdf report, and attachments of the report
# Input:
# reportList -> json data returned by getReportList method
# CONFIG -> the loaded config data, to use the correct APIs
# Output:
# Progress printed to console
def getReport(reportList, CONFIG):
    for report in reportList:
        reportID = str(report["report_id"])
        print("Downloading Web Content For Report ID: " + reportID)
        url = report["url"]
        response = timeout(url)
        if not response:
            print("HTML File Not Found.")
            print("Continue to Check PDF File...")
        else:
            dirpath = "reports/" + reportID + "/html/"
            if not os.path.exists(os.path.dirname(dirpath)):
                os.makedirs(os.path.dirname(dirpath))
            with open(dirpath + "web.txt", "w+") as f:
                f.write(response.content.decode("utf-8", errors="ignore"))
            print("Done Downloading HTML File.")
        print("Checking PDF For Report ID: " + reportID)
        resp = timeout(CONFIG["GET_REPORT"] + reportID)
        if not resp:
            print("PDF Report Does Not Exist.")
            print("Continue to Check Attachment.")
        else:
            content = json.loads(resp.content)
            pdfURL = content["pdf_url"]
            print("PDF Found! Downloading Now...")
            pdfDirpath = "reports/" + reportID + "/pdf/"
            if not os.path.exists(os.path.dirname(pdfDirpath)):
                os.makedirs(os.path.dirname(pdfDirpath))
            wget.download(pdfURL, pdfDirpath)
            print("\nDone Downloading PDF.")
        print("Checking Attachment For Report ID: " + reportID)
        res = timeout(CONFIG["GET_REPORT_ATTACHMENT"] + reportID)
        if res.content != bytes("[]", "utf-8"):
            attachmentList = json.loads(res.content)
            print(
                "     Attachment Found! Total "
                + str(len(attachmentList))
                + " Attachment(s)"
            )
            attachDirpath = "reports/" + reportID + "/attachment/"
            if not os.path.exists(os.path.dirname(attachDirpath)):
                os.makedirs(os.path.dirname(attachDirpath))
            for index, attachment in enumerate(attachmentList):
                print("         Downloading " + str(index + 1) + "...")
                wget.download(attachment["attachment_url"], attachDirpath)
                print("         Done.")
            print("     Done Downloading Attachments.")
            print(
                "========================================================================================="
            )
        else:
            print("     Attachment Not Found For: " + reportID)
            print("     Continue to Next Report...")
            print(
                "========================================================================================="
            )


# GRDC APIs have restrictions on the frequency of calling the APIs, around 1-2.5s per request, use this method to delay the request and avoid 429
# Input:
# url -> the request url
# Output:
# response -> the response from requesting the url
def timeout(url):
    while True:
        try:
            time.sleep(2)
            response = requests.get(url)
            if response.status_code == 404:
                return None
            while response.status_code != 200:
                time.sleep(2)
                response = requests.get(url)
            return response
        except:
            time.sleep(4)


def buildJSON(reportlist, CONFIG):
    JSON_PREFIX = 'json/'
    for i, report in enumerate(reportlist):
        report_id = report['report_id']
        print("Processing Report: {}, {}/{}".format(report_id, i + 1, len(reportlist)))
        report_detail = getReportDetails(report_id, CONFIG)
        report_status = getReportStatus(report_id, CONFIG)
        report_category = getReportCategory(report_id, CONFIG)
        if len(report_category) == 0:
            report_category = [{
                'category_name': None,
                'parent_category_name': None
            }]
        attachmentJSON = getAttachmentJSON(report_id, CONFIG)
        JSONReport = assignPDFDetail(report, report_detail, report_status, report_category, attachmentJSON)
        with open('{}{}.json'.format(JSON_PREFIX, report_id), 'w') as f:
            json.dump(JSONReport, f)


def assignPDFDetail(report, report_detail, report_status, report_category, attachmentJSON):
    PDF_PATH_PREFIX = 'reports/{}/pdf/'
    report_full_text_content = ''
    pdfPath = PDF_PATH_PREFIX.format(report['report_id'])
    if os.path.exists(os.path.dirname(pdfPath)):
        dirs = os.listdir(pdfPath)
        for d in dirs:
            if d != '.DS_Store':
                report_full_text_content = extractPDF('{}{}'.format(pdfPath, d))
    JSONReport = {
        'report_id': report['report_id'],
        'project_number': report['project_number'],
        'report_title': report['report_title'],
        'region_name': report['region_name'],
        'organisation_name': report['organisation_name'],
        'commence_date': report['commence_date'],
        'complete_date': report['complete_date'],
        'publish_date': report['publish_date'],
        'report_type': report['report_type'],
        'supervisor_name': report['supervisor_name'],
        'state': report['state'],
        'keywords': report['keywords'].split(', '),
        'report_summary': report['report_summary'],
        'report_status': report_status['status'],
        'pdf_url': report_detail['pdf_url'],
        'web_url': report_detail['url'],
        'report_achievement': report_detail['report_achievement'],
        'report_conclusion': report_detail['report_conclusion'],
        'report_outcome': report_detail['report_outcome'],
        'report_recommendation': report_detail['report_recommendation'],
        'report_discussion': report_detail['report_discussion'],
        'other_research': report_detail['other_research'],
        'ip_summary': report_detail['ip_summary'],
        'additional_information': report_detail['additional_information'],
        'report_full_text_content': report_full_text_content,
        'category_name': report_category[0]['category_name'],
        'research_theme_name': report_category[0]['parent_category_name'],
        'html_content': getHTMLContent(report['report_id']),
        'attachments': attachmentJSON
    }
    return JSONReport


def extractPDF(path):
    raw = parser.from_file(path)
    if raw['content']:
        return raw['content'].strip()
    else:
        return None


def getReportDetails(report_id, CONFIG):
    url = CONFIG['GET_REPORT'].format(report_id)
    respose = timeout(url)
    return json.loads(respose.content)


def getReportStatus(report_id, CONFIG):
    url = CONFIG['GET_REPORT_STATUS'].format(report_id)
    response = timeout(url)
    return json.loads(response.content)


def getReportCategory(report_id, CONFIG):
    url = CONFIG['GET_REPORT_CATEGORY'].format(report_id)
    response = timeout(url)
    return json.loads(response.content)


def getHTMLContent(report_id):
    HTML_PATH_PREFIX = 'reports/{}/html/'
    html_content = ''
    htmlpath = HTML_PATH_PREFIX.format(report_id)
    if os.path.exists(os.path.dirname(htmlpath)):
        dirs = os.listdir(htmlpath)
        for d in dirs:
            if d != '.DS_Store':
                with open('{}web.txt'.format(htmlpath), 'r') as f:
                    html_content = f.read()
    return html_content


def getAttachmentJSON(report_id, CONFIG):
    attachments = []
    ATTACHMENT_PATH_PREFIX = 'reports/{}/attachment/'
    attachpath = ATTACHMENT_PATH_PREFIX.format(report_id)
    if os.path.exists(os.path.dirname(attachpath)):
        attachment_details = getAttachmentDetails(report_id, CONFIG)
        for attachment in attachment_details:
            attachment['file_name'] = attachment['file_name'].split('.')[0]
        dirs = os.listdir(attachpath)
        for d in dirs:
            if d != '.DS_Store':
                attachment_detail = {}
                for a in attachment_details:
                    fname = d.split('.')[0].strip()
                    if a['file_name'].strip() == fname:
                        attachment_detail = a
                attach_path = '{}{}'.format(attachpath, d)
                attachment_content = extractPDF(attach_path)
                base64_content = getAttachmentBase64Content(attachment_detail['attachment_id'], CONFIG)
                attachment = {
                    'report_id': report_id,
                    'attachment_full_text_content': attachment_content,
                    'attachment_name': attachment_detail['file_name'],
                    'attachment_id': attachment_detail['attachment_id'],
                    'attachment_size': attachment_detail['file_size'],
                    'attachment_type': attachment_detail['file_type'],
                    'attachment_url': attachment_detail['attachment_url'],
                    'attachment_base64_content': base64_content
                }
                attachments.append(attachment)
    return attachments


def getAttachmentDetails(report_id, CONFIG):
    url = CONFIG['GET_REPORT_ATTACHMENT'].format(report_id)
    response = timeout(url)
    return json.loads(response.content)


def getAttachmentBase64Content(attachment_id, CONFIG):
    url = CONFIG['GET_REPORT_ATTACHMENT_CONTENT'].format(attachment_id)
    response = timeout(url)
    content = json.loads(response.content)
    return content['base64_content']


def cleanJSONFiles(CONFIG):
    path = CONFIG["JSON_PATH"]
    files = os.listdir(path)
    for file in files:
        if file != ".DS_Store":
            print("Processing " + file + " ...")
            with open(path + file, "r", encoding="utf-8") as jsonfile:
                jf = json.loads(jsonfile.read())
            html_content = jf["html_content"]
            full_text = jf["report_full_text_content"]
            full_text = full_text.replace("\n", " ")
            full_text = ' '.join(full_text.split())
            attachments = jf["attachments"]
            if len(attachments) > 0:
                for attachment in attachments:
                    if attachment["attachment_full_text_content"] is not None:
                        attachment_content = attachment["attachment_full_text_content"]
                        attachment_content = attachment_content.replace("\n", " ")
                        attachment_content = ' '.join(attachment_content.split())
                        attachment["attachment_full_text_content"] = attachment_content
            soup = BeautifulSoup(html_content, 'lxml')
            for s in soup.select('script'):
                s.decompose()
            for s in soup.select('style'):
                s.decompose()
            for s in soup.select('#footer'):
                s.decompose()
            cleaned_HTML = soup.get_text()
            cleaned_HTML.replace("\t", " ")
            res = ' '.join(cleaned_HTML.split())
            jf["html_content"] = res
            jf["report_full_text_content"] = full_text
            jf["attachments"] = attachments
            with open(path + file, 'w') as f:
                json.dump(jf, f)
            print("Done with " + file)


def splitContents(CONFIG):
    path = CONFIG["JSON_PATH"]
    files = os.listdir(path)
    for file in files:
        if file != ".DS_Store":
            print("Processing " + file + " ...")
            with open(path + file, "r", encoding="utf-8") as jsonfile:
                jf = json.loads(jsonfile.read())
            html_content = jf["html_content"]
            splited_html_content = html_content.split('. ')
            html_portion = int(round(len(splited_html_content) / 3))
            html_concate_1 = '. '.join(splited_html_content[:html_portion]) + '.'
            html_concate_2 = '. '.join(splited_html_content[html_portion:html_portion + html_portion]) + '.'
            html_concate_3 = '. '.join(splited_html_content[html_portion + html_portion:]) + '.'
            concated_html_content = [html_concate_1, html_concate_2, html_concate_3]
            jf["html_content"] = concated_html_content

            full_text = jf["report_full_text_content"]
            splited_full_content = full_text.split('. ')
            full_portion = int(round(len(splited_full_content) / 3))
            full_concate_1 = '. '.join(splited_full_content[:full_portion]) + '.'
            full_concate_2 = '. '.join(splited_full_content[full_portion:full_portion + full_portion]) + '.'
            full_concate_3 = '. '.join(splited_full_content[full_portion + full_portion:]) + '.'
            concated_full_content = [full_concate_1, full_concate_2, full_concate_3]
            jf["report_full_text_content"] = concated_full_content

            report_discussion = jf["report_discussion"]
            if report_discussion is not None:
                concated_dis_content = []
                splited_discussion = report_discussion.split('. ')
                dis_portion = int(round(len(splited_discussion) / 3))
                dis_concate_1 = '. '.join(splited_discussion[:dis_portion]) + '.'
                dis_concate_2 = '. '.join(splited_discussion[dis_portion:dis_portion + dis_portion]) + '.'
                dis_concate_3 = '. '.join(splited_discussion[dis_portion + dis_portion:]) + '.'

                temp = [dis_concate_1, dis_concate_2, dis_concate_3]

                for each in temp:
                    if len(each.encode(encoding='UTF-8', errors='strict')) < 32766:
                        concated_dis_content.append(each)
                    else:
                        inner_splited_dis = each.split(' ')
                        inner_dis_portion = int(round(len(inner_splited_dis) / 3))
                        inner_dis_concate_1 = ' '.join(inner_splited_dis[:inner_dis_portion]) + ' '
                        inner_dis_concate_2 = ' '.join(
                            inner_splited_dis[inner_dis_portion:inner_dis_portion * 2]) + ' '
                        inner_dis_concate_3 = ' '.join(
                            inner_splited_dis[inner_dis_portion * 2:]) + ' '

                        concated_dis_content.append(inner_dis_concate_1)
                        concated_dis_content.append(inner_dis_concate_2)
                        concated_dis_content.append(inner_dis_concate_3)

                jf["report_discussion"] = concated_dis_content
            else:
                jf["report_discussion"] = []

            additional_information = jf["additional_information"]
            if additional_information is not None:
                concated_info_content = []
                splited_info = additional_information.split('. ')
                info_portion = int(round(len(splited_info) / 3))
                info_concate_1 = '. '.join(splited_info[:info_portion]) + '.'
                info_concate_2 = '. '.join(splited_info[info_portion:info_portion + info_portion]) + '.'
                info_concate_3 = '. '.join(splited_info[info_portion + info_portion:]) + '.'

                temp = [info_concate_1, info_concate_2, info_concate_3]

                for each in temp:
                    if len(each.encode(encoding='UTF-8', errors='strict')) < 32766:
                        concated_info_content.append(each)
                    else:
                        inner_splited_info = each.split(' ')
                        inner_info_portion = int(round(len(inner_splited_info) / 3))
                        inner_info_concate_1 = ' '.join(inner_splited_info[:inner_info_portion]) + ' '
                        inner_info_concate_2 = ' '.join(
                            inner_splited_info[inner_info_portion:inner_info_portion * 2]) + ' '
                        inner_info_concate_3 = ' '.join(
                            inner_splited_info[inner_info_portion * 2:]) + ' '

                        concated_info_content.append(inner_info_concate_1)
                        concated_info_content.append(inner_info_concate_2)
                        concated_info_content.append(inner_info_concate_3)

                jf["additional_information"] = concated_info_content
            else:
                jf["additional_information"] = []

            report_achievement = jf["report_achievement"]
            if report_achievement is not None:
                splited_achievement = report_achievement.split('. ')
                ach_portion = int(round(len(splited_achievement) / 3))
                ach_concate_1 = '. '.join(splited_achievement[:ach_portion]) + '.'
                ach_concate_2 = '. '.join(splited_achievement[ach_portion:ach_portion + ach_portion]) + '.'
                ach_concate_3 = '. '.join(splited_achievement[ach_portion + ach_portion:]) + '.'
                concated_ach_content = [ach_concate_1, ach_concate_2, ach_concate_3]
                jf["report_achievement"] = concated_ach_content
            else:
                jf["report_achievement"] = []

            report_conclusion = jf["report_conclusion"]
            if report_conclusion is not None:
                splited_conclusion = report_conclusion.split('. ')
                con_portion = int(round(len(splited_conclusion) / 3))
                con_concate_1 = '. '.join(splited_conclusion[:con_portion]) + '.'
                con_concate_2 = '. '.join(splited_conclusion[con_portion:con_portion + con_portion]) + '.'
                con_concate_3 = '. '.join(splited_conclusion[con_portion + con_portion:]) + '.'
                concated_con_content = [con_concate_1, con_concate_2, con_concate_3]
                jf["report_conclusion"] = concated_con_content
            else:
                jf["report_conclusion"] = []

            report_outcome = jf["report_outcome"]
            if report_outcome is not None:
                splited_outcome = report_outcome.split('. ')
                outcome_portion = int(round(len(splited_outcome) / 3))
                outcome_concate_1 = '. '.join(splited_outcome[:outcome_portion]) + '.'
                outcome_concate_2 = '. '.join(splited_outcome[outcome_portion:outcome_portion + outcome_portion]) + '.'
                outcome_concate_3 = '. '.join(splited_outcome[outcome_portion + outcome_portion:]) + '.'
                concated_outcome_content = [outcome_concate_1, outcome_concate_2, outcome_concate_3]
                jf["report_outcome"] = concated_outcome_content
            else:
                jf["report_outcome"] = []

            report_recommendation = jf["report_recommendation"]
            if report_recommendation is not None:
                splited_rec = report_recommendation.split('. ')
                rec_portion = int(round(len(splited_rec) / 3))
                rec_concate_1 = '. '.join(splited_rec[:rec_portion]) + '.'
                rec_concate_2 = '. '.join(splited_rec[rec_portion:rec_portion + rec_portion]) + '.'
                rec_concate_3 = '. '.join(splited_rec[rec_portion + rec_portion:]) + '.'
                concated_rec_content = [rec_concate_1, rec_concate_2, rec_concate_3]
                jf["report_recommendation"] = concated_rec_content
            else:
                jf["report_recommendation"] = []

            other_research = jf["other_research"]
            if other_research is not None:
                splited_or = other_research.split('. ')
                or_portion = int(round(len(splited_or) / 3))
                or_concate_1 = '. '.join(splited_or[:or_portion]) + '.'
                or_concate_2 = '. '.join(splited_or[or_portion:or_portion + or_portion]) + '.'
                or_concate_3 = '. '.join(splited_or[or_portion + or_portion:]) + '.'
                concated_or_content = [or_concate_1, or_concate_2, or_concate_3]
                jf["other_research"] = concated_or_content
            else:
                jf["other_research"] = []

            report_summary = jf["report_summary"]
            if report_summary is not None:
                splited_sum = report_summary.split('. ')
                sum_portion = int(round(len(splited_sum) / 3))
                sum_concate_1 = '. '.join(splited_sum[:sum_portion]) + '.'
                sum_concate_2 = '. '.join(splited_sum[sum_portion:sum_portion + sum_portion]) + '.'
                sum_concate_3 = '. '.join(splited_sum[sum_portion + sum_portion:]) + '.'
                concated_sum_content = [sum_concate_1, sum_concate_2, sum_concate_3]
                jf["report_summary"] = concated_sum_content
            else:
                jf["report_summary"] = []

            attachments = jf["attachments"]
            if len(attachments) > 0:
                for attachment in attachments:
                    if attachment["attachment_full_text_content"] is not None:
                        attachment_content = attachment["attachment_full_text_content"]
                        concated_attachment_content = []
                        splited_attachment_content = attachment_content.split('. ')
                        attachment_portion = int(round(len(splited_attachment_content) / 3))
                        attachment_concate_1 = '. '.join(splited_attachment_content[:attachment_portion]) + '.'
                        attachment_concate_2 = '. '.join(splited_attachment_content[attachment_portion:attachment_portion + attachment_portion]) + '.'
                        attachment_concate_3 = '. '.join(splited_attachment_content[attachment_portion + attachment_portion:]) + '.'

                        temp = [attachment_concate_1, attachment_concate_2, attachment_concate_3]

                        for each in temp:
                            if len(each.encode(encoding='UTF-8', errors='strict')) < 32766:
                                concated_attachment_content.append(each)
                            else:
                                inner_splited_attachment = each.split(' ')
                                inner_attachment_portion = int(round(len(inner_splited_attachment) / 4))
                                inner_attachment_concate_1 = ' '.join(inner_splited_attachment[:inner_attachment_portion]) + ' '
                                inner_attachment_concate_2 = ' '.join(inner_splited_attachment[inner_attachment_portion:inner_attachment_portion*2]) + ' '
                                inner_attachment_concate_3 = ' '.join(inner_splited_attachment[inner_attachment_portion*2:inner_attachment_portion*3]) + ' '
                                inner_attachment_concate_4 = ' '.join(inner_splited_attachment[inner_attachment_portion*3:]) + ' '
                                concated_attachment_content.append(inner_attachment_concate_1)
                                concated_attachment_content.append(inner_attachment_concate_2)
                                concated_attachment_content.append(inner_attachment_concate_3)
                                concated_attachment_content.append(inner_attachment_concate_4)

                        jf["attachment_full_text_content"] = concated_attachment_content
                    else:
                        jf["attachment_full_text_content"] = []
            jf["attachments"] = attachments

            with open(path + file, 'w') as f:
                json.dump(jf, f)
            print("Done with " + file)
