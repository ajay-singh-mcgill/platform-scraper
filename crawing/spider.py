import datetime

import sys
import os
from selenium.webdriver.firefox.options import Options

# This needs to be updated for every environment
#sys.path.append("/Users/ajaysingh/PycharmProjects/platform_scraper")
sys.path.append("/home/crawler/appexchange/")

from constants import page_load_wait_time, category_url_dict, app_overview_tab_base_url, output_file_header, \
    category_page_show_more_button_id, category_page_app_matrix_id, gecko_logpath, executable_path, data_folder_path

sys.path.append(gecko_logpath)

from urllib.request import urlopen
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, NoSuchWindowException

import time
import parsing.app_page_parse as parsing_util
import re

import logging

from multiprocessing.dummy import Pool as ThreadPool

counter = 0

gecko_logpath = gecko_logpath+"geckolog.log"

# Get all the child-apps url link from the category page
def get_category_apps_list(url):
    print('inside the func')
    app_url_list = []
    options = Options()
    options.headless = True
    print(options)
    driver = webdriver.Firefox(options=options, log_path=gecko_logpath, executable_path=executable_path)
    try:
        print(url)
        driver.implicitly_wait(page_load_wait_time)
        driver.get(url)
        python_button = driver.find_element_by_id(category_page_show_more_button_id)
        while python_button:
            try:
                python_button.click()
                print('clicking')
                time.sleep(page_load_wait_time)
                python_button = driver.find_element_by_id(category_page_show_more_button_id)
            except ElementNotInteractableException as e:
                break
        soup=BeautifulSoup(driver.page_source, 'lxml')
        productDivs = soup.find('ul', attrs={'id' : category_page_app_matrix_id})
        for href in productDivs.find_all('a'):
            app_url_list.append(href['href'])
        return app_url_list
    except Exception as e:
        print("Error occured while getting the child list for the url: "+url)
        print(e)
    finally:
        driver.close()

def get_app_listing_id(url):
    return (str(url).split('listingId=')[1])

def get_app_overview_details(app_listing_id):
    # Get the information for the overview tab in the app page by making a GET call
    if app_listing_id:
        child_overview_url = app_overview_tab_base_url+app_listing_id
        try:
            child_overview_html = urlopen(child_overview_url)
            child_overview_soup = BeautifulSoup(child_overview_html, 'lxml')
            app_overview_details = parsing_util.parse_app_page_overview_tab(child_overview_soup)
            return app_overview_details
        except Exception as e:
            return ""
    else: return ""

# Get the app specific data and the data in the overview tab of the app page
def get_app_data(input):
    # Get the information from the app page top section
    category_url = input['category_url']
    logger = input['logger']
    try:
        print('Getting child list')
        child_url_list = get_category_apps_list(category_url)
    except NoSuchWindowException as e:
        print("Error in getting child list for the category: "+category_url)
        print(e)
    if child_url_list:
        child_url_list = set(child_url_list)
        print(category_url, ":", len(child_url_list))
        for url in child_url_list:
            child_html = urlopen(url)
            child_soup = BeautifulSoup(child_html, 'lxml')
            if child_soup:
                app_page_title = re.sub('<[^>]*>', '', str(child_soup.title))
                app_listing_id =  get_app_listing_id(url)
                app_details = parsing_util.parse_app_page_data(child_soup)
                app_meta_details = "~".join([str(app_page_title),app_listing_id,url])
                app_overview_details = get_app_overview_details(app_listing_id)
                final_app_details = "~".join([app_meta_details, app_details, app_overview_details])
                write_app_details_to_file(final_app_details, logger)

def initialize_output_file():
    filename =str(datetime.datetime.now())+".csv"
    filepath = data_folder_path+filename
    logger = initialize_logger(filepath)
    os.environ['output_file'] = filepath
    f = open(filepath, 'w')
    f.write(output_file_header)
    f.close()
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
    print('Starting')
    category_url_list = category_url_dict.values()
    print(category_url_list)
    pool = ThreadPool(4)
    logger = initialize_output_file()
    input_list = [{'category_url': url, 'logger': logger} for url in category_url_list]
    pool.map(get_app_data, input_list)
    pool.close()
    pool.join()
