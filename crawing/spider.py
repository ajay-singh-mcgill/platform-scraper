import datetime

import constants

from urllib.request import urlopen
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

import time
import parsing.app_page_parse as parsing_util

import urllib
from multiprocessing.dummy import Pool as ThreadPool

def get_reviews_data(url):
    try:
        driver = webdriver.Firefox()
        driver.implicitly_wait(constants.page_load_wait_time)
        driver.get(url)
        python_button = driver.find_element_by_id('tab-default-2__item')
        while python_button:
            try:
                python_button.click()
                time.sleep(5)
                driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                python_button = driver.find_element_by_class_name('slds-button slds-button_neutral')
            except ElementNotInteractableException as e:
                break
            except NoSuchElementException as e:
                break
        soup = BeautifulSoup(driver.page_source, 'lxml')
        print(soup)
    except NoSuchElementException as e:
        print(e)
    finally:
        driver.close()

# Get all the child-apps url link from the category page
def get_category_apps_list(url):
    app_url_list = []
    try:
        driver = webdriver.Firefox()
        driver.implicitly_wait(constants.page_load_wait_time)
        driver.get(url)
        python_button = driver.find_element_by_id(constants.category_page_show_more_button_id)
        while python_button:
            try:
                python_button.click()
                time.sleep(constants.page_load_wait_time)
                python_button = driver.find_element_by_id(constants.category_page_show_more_button_id)
            except ElementNotInteractableException as e:
                break

        soup=BeautifulSoup(driver.page_source, 'lxml')
        productDivs = soup.find('ul', attrs={'id' : constants.category_page_app_matrix_id})
        for href in productDivs.find_all('a'):
            app_url_list.append(href['href'])
        return app_url_list
    except Exception as e:
        print(e)
    finally:
        driver.close()

def get_app_listing_id(url):
    return (str(url).split('listingId=')[1])

# Get the app specific data and the data in the overview tab of the app page
def get_app_data(url):

    # Get the information from the app page top section
    child_html = urlopen(url)
    child_soup = BeautifulSoup(child_html, 'lxml')
    app_page_title = child_soup.title
    app_listing_id =  get_app_listing_id(url)
    app_details = parsing_util.parse_app_page_data(url)
    app_meta_details = ",".join([str(app_page_title),app_listing_id,url])

    # Get the information for the overview tab in the app page by making a GET call
    child_overview_url = constants.app_overview_tab_base_url+app_listing_id
    child_overview_html = urlopen(child_overview_url)
    child_overview_soup = BeautifulSoup(child_overview_html, 'lxml')
    app_overview_details = parsing_util.parse_app_page_overview_tab(child_overview_soup)
    final_app_details = ",".join(app_meta_details, app_details, app_overview_details)
    return final_app_details

def initialize_output_file():
    filename =str(datetime.datetime.now())+".csv"
    f = open(filename, 'w')
    f.write(constants.output_file_header)
    f.close()

if __name__ == '__main__':
    url_list = constants.category_url_dict.values()
    pool = ThreadPool(3)
    pool.map(urllib.request.urlopen, url_list)
    initialize_output_file()


urls = [
  'http://www.python.org',
  'http://www.python.org/about/',
  'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
  'http://www.python.org/doc/',
  'http://www.python.org/download/',
  'http://www.python.org/getit/',
  'http://www.python.org/community/',
  'https://wiki.python.org/moin/',
]

# make the Pool of workers
pool = ThreadPool(3)

# open the urls in their own threads
# and return the results
results = pool.map(urllib.request.urlopen, urls)

# close the pool and wait for the work to finish
pool.close()
pool.join()

for result in results:
    print(result.url)