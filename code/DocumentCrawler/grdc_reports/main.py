import sys
from methods import *

print("---------------------------------------------------------")
print("Loading Config...")
CONFIGFILE = open("config.json", "r")
CONFIG = json.loads(CONFIGFILE.read())
CONFIGFILE.close()
print("Loaded.")
print("---------------------------------------------------------")


def extractFromAPI():
    report_list = None
    while report_list is None or report_list is []:
        report_list = getReportList(CONFIG)
    getReport(report_list, CONFIG)


def extractPDF2JSON():
    report_list = None
    while report_list is None or report_list is []:
        report_list = getReportList(CONFIG)
    buildJSON(report_list, CONFIG)


def cleanJSON():
    cleanJSONFiles(CONFIG)


def splitFileContents():
    splitContents(CONFIG)


if __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) == 2 and (arguments[1] == "--extract" or arguments[1] == "-e"):
        extractPDF2JSON()
    elif len(arguments) == 2 and (arguments[1] == "--download" or arguments[1] == "-d"):
        extractFromAPI()
    elif len(arguments) == 2 and (arguments[1] == "--clean" or arguments[1] == "-c"):
        cleanJSON()
    elif len(arguments) == 2 and (arguments[1] == "--split" or arguments[1] == "-s"):
        splitFileContents()
    else:
        print("Wrong arguments.")
        print("-e or --extract  ---> extract pdf to json")
        print("-d or --download ---> download reports from API")
        print("-c or --clean    ---> clean the contents")
