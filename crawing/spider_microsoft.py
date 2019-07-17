import datetime

import sys
import os

import requests

# This needs to be updated for every environment
sys.path.append("/Users/ajaysingh/PycharmProjects/platform_scraper")

from constants import microsoft_category_url_dict, microsoft_file_header, microsoft_data_folder_path, \
    microsoft_base_url, microsoft_app_price_url

from urllib.request import urlopen
from bs4 import BeautifulSoup

import parsing.microsoft_parsing as parsing_util
import re

import logging

from multiprocessing.dummy import Pool as ThreadPool

counter = 0

# Get all the child-apps url link from the category page
def get_category_apps_list(url):
    final_child_app_ids = []
    productDivs = ""
    page_number = 1
    base_url = url
    while productDivs is not None:
        url = base_url+"&page="+str(page_number)
        category_html = urlopen(url)
        soup=BeautifulSoup(category_html, 'lxml')
        productDivs = soup.find('div', attrs={'class' : 'spza_filteredTileContainer'})
        if productDivs:
            child_app_ids = re.findall(r'<a href=\"(.*?)\"', str(productDivs))
            final_child_app_ids = final_child_app_ids + child_app_ids
            print(len(final_child_app_ids))
            page_number +=1
        else:
            return final_child_app_ids

def get_app_data(input):
    category_url = input['category_url']
    logger = input['logger']
    try:
        child_url_list = get_category_apps_list(category_url)
    except Exception as e:
        print(e)
    child_url_list = set(child_url_list)
    print(category_url, ":", len(child_url_list))
    if child_url_list:
        for child_url in child_url_list:
            if not child_url:
                continue
            url = microsoft_base_url+child_url
            try:
                child_html = urlopen(url)
            except Exception as e:
                print(e)
                continue
            child_soup = BeautifulSoup(child_html, 'lxml')
            if child_soup:
                app_details = parsing_util.parse_app_details(child_soup)
                app_id = "NA"
                if re.findall('\/(.*)\?tab=Overview', url):
                    app_id = re.findall('\/(.*)\?tab=Overview', url)[0]
                    app_id = app_id.split("/")[-1]
                final_app_details = "~".join([app_details, url, app_id])
                write_app_details_to_file(final_app_details, logger)
    else:
        print("No children apps found for the category: "+input)

def get_price_data():
    response = requests.get(microsoft_app_price_url)
    if response.status_code == 200:
        return response.content
    else:
        return False

def initialize_output_file():
    filename =str(datetime.datetime.now())+".csv"
    filepath = microsoft_data_folder_path+filename
    price_file = "app_price_"+filename
    price_filepath = microsoft_data_folder_path+price_file
    logger = initialize_logger(filepath)
    os.environ['output_file'] = filepath
    f = open(filepath, 'w')
    f.write(microsoft_file_header)
    f.close()
    price_data = get_price_data()
    if price_data:
        try:
            f = open(price_filepath, 'w')
            f.write(str(price_data))
        finally:
            f.close()
    else:
        raise ValueError('No price data found; exiting!')
    return logger

def write_app_details_to_file(output_line, logger):
    global counter
    counter = counter + 1
    if counter%10 == 0:
        print(str(datetime.datetime.now())+"----->"+str(counter))
    if logger:
        logger.info(output_line)

#Using logger for file operations to make them thread-safe
def initialize_logger(filename):
    logpath = filename
    logger = logging.getLogger('log')
    logger.setLevel(logging.INFO)
    ch = logging.FileHandler(logpath)
    ch.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(ch)
    return logger

if __name__ == '__main__':
    category_url_list = microsoft_category_url_dict.values()
    pool = ThreadPool(4)
    logger = initialize_output_file()
    input_list = [{'category_url': url, 'logger': logger} for url in category_url_list]
    pool.map(get_app_data, input_list)
    pool.close()
    pool.join()