import datetime
import glob
from dateutil import parser

def sortDeveloperFileNamesByDate(developerFileNames):
    final_list = []
    for file in developerFileNames:
        entry = {'filename': file,
                 'date': file.split("(")[1].split(")")[0].strip(" ")}
        entry['date'] = datetime.datetime.strftime(parser.parse(entry['date']), '%m/%d/%Y')
        final_list.append(entry)
    final_list = sorted(final_list, key=lambda x:datetime.datetime.strptime(x['date'], '%m/%d/%Y'))
    return final_list


def getDeveloperDataFiles(dataFiles, key):
    developer_list = []
    for file in dataFiles:
        if key in file:
            developer_list.append(file)
    return developer_list