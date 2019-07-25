import datetime

import sys
import os
from selenium.webdriver.firefox.options import Options

sys.path.append("/Users/ajaysingh/PycharmProjects/platform_scraper")

from constants import page_load_wait_time, category_url_dict, salesforce_review_data_file_header, \
    category_page_show_more_button_id, category_page_app_matrix_id, gecko_logpath, executable_path, \
    salesforce_review_data_folder

sys.path.append(gecko_logpath)

from urllib.request import urlopen
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, NoSuchWindowException

import time
import re

import logging

from multiprocessing.dummy import Pool as ThreadPool

counter = 0

gecko_logpath = gecko_logpath+"geckolog.log"

def get_reviews_data(url, app_id):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, log_path=gecko_logpath, executable_path=executable_path)
    final_reviews = []
    try:
        driver.implicitly_wait(page_load_wait_time)
        driver.get(url)
        python_button = driver.find_element_by_id('tab-default-2__item')
        while python_button:
            try:
                python_button.click()
                time.sleep(5)
                driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                python_button = driver.find_element_by_id('appx_load_more_button')
                time.sleep(3)
            except ElementNotInteractableException as e:
                break
            except NoSuchElementException as e:
                break
        soup = BeautifulSoup(driver.page_source, 'lxml')
        reviews_container = soup.find('div', attrs={'id': 'appxRevsContainer'})
        reviews_raw = re.findall('div class=\"appx-review\"(.*)>', str(reviews_container))
        if reviews_raw:
            for review_raw in reviews_raw[1:]:
                review_id = review_raw.split("data-revid=\"")[1].split("\">")[0]
                reviewer_details = review_raw.split("href=\"/profile?u=")[1].split("</a>")[0]
                reviewer_id = reviewer_details.split("\">")[0]
                reviewer_name = reviewer_details.split("\">")[1]
                rating_stars = review_raw.split("appx-rating-stars-")[1].split("\"")[0]
                review_date = review_raw.split(");\">")[1].split("</a>")[0]
                review_title = review_raw.split("appx-review-title\">")[1].split("</p>")[0]
                review_description = review_raw.split("appx-multi-line-fixed\">")[1].split("</p>")[0]
                review_data = {'review_id': review_id,
                 'reviewer_id': reviewer_id,
                 'reviewer_name': reviewer_name,
                 'rating_stars': rating_stars,
                 'review_date': review_date,
                 'review_title': review_title,
                 'review_description': review_description}
                print(review_data)
                final_reviews.append(review_data)
        final_data = "~".join([url, app_id, str(final_reviews)])
        return final_data
    except NoSuchElementException as e:
        print(e)
    finally:
        driver.close()

# Get all the child-apps url link from the category page
def get_category_apps_list(url):
    app_url_list = []
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, log_path=gecko_logpath, executable_path=executable_path)
    try:
        driver.implicitly_wait(page_load_wait_time)
        driver.get(url)
        python_button = driver.find_element_by_id(category_page_show_more_button_id)
        while python_button:
            try:
                python_button.click()
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

# Get the app specific data and the data in the overview tab of the app page
def get_app_data(input):
    category_url = input['category_url']
    logger = input['logger']
    try:
        child_url_list = get_category_apps_list(category_url)
    except NoSuchWindowException as e:
        print("Error in getting child list for the category: "+category_url)
        print(e)
    if child_url_list:
        print(category_url, ":", len(child_url_list))
        child_url_list = set(child_url_list)
        print(category_url, ":", len(child_url_list))
        for url in child_url_list:
            print(url)
            app_listing_id = get_app_listing_id(url)
            review_data = get_reviews_data(url, app_listing_id)
            write_app_details_to_file(review_data, logger)

def initialize_output_file():
    filename =str(datetime.datetime.now())+".csv"
    filepath = salesforce_review_data_folder+filename
    logger = initialize_logger(filepath)
    os.environ['output_file'] = filepath
    f = open(filepath, 'w')
    f.write(salesforce_review_data_file_header)
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
    category_url_list = category_url_dict.values()
    pool = ThreadPool(4)
    logger = initialize_output_file()
    input_list = [{'category_url': url, 'logger': logger} for url in category_url_list]
    pool.map(get_app_data, input_list)
    pool.close()
    pool.join()
