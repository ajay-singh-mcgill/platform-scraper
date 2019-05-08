import csv
import datetime
import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrapeAppListingURLs(url, browser, first_pageload=False):

    app_urls = []
    featured_urls = []

    browser.get(url)

    if first_pageload is True:
        cookie_cross = browser.find_element_by_id('appx_cookie_banner_eu_close')
        browser.execute_script("arguments[0].scrollIntoView();", cookie_cross)
        cookie_cross.click()
        
    app_featured_list = browser.find_element_by_id('j_id0:AppxLayout:LandingPage:landingpage:page_sections:1:j_id1852')

    featured_app_link_elements = app_featured_list.find_elements_by_tag_name('a')

    for featured_app_link_element in featured_app_link_elements:

        featured_app_link = featured_app_link_element.get_attribute('href')

        if featured_app_link not in featured_urls:

            featured_urls.append(featured_app_link)

    total_apps = int(browser.find_element_by_id('total-items-store').text)
    
    print(len(featured_urls))
    print(total_apps)

    while len(app_urls) < total_apps:

        app_list = browser.find_element_by_id('j_id0:AppxLayout:listings')

        app_link_elements = app_list.find_elements_by_tag_name('a')

        for app_link_element in app_link_elements:

            app_url = app_link_element.get_attribute('href')

            if app_url not in app_urls:

                app_urls.append(app_url)
        print(len(app_urls))
        
        if len(app_urls) < total_apps:
        
            load_more_button = browser.find_element_by_id('appx-load-more-button-id')
        
            browser.execute_script("arguments[0].scrollIntoView();", load_more_button)
            
            load_more_button.click()

            time.sleep(10)

    return app_urls, featured_urls

def scrapeAppListingPage(url, browser, featured_urls, category, rank, app_data, provider_data, review_data):

    browser.get(url)

    time.sleep(10)

    try:
        provider = browser.find_element_by_class_name('appx-company-name').text
    except selenium.common.exceptions.NoSuchElementException:
        try:
            time.sleep(60)
            provider = browser.find_element_by_class_name('appx-company-name').text
        except selenium.common.exceptions.NoSuchElementException:
            attempts = 0
            provider = ''
            while attempts < 5 and provider == '':
                browser.get(url)
                time.sleep(10)
                try:
                    provider = browser.find_element_by_class_name('appx-company-name').text
                except selenium.common.exceptions.NoSuchElementException:
                    attempts = attempts + 1

    coded_provider_data = [d for d in provider_data if d['provider_name'] == provider]

    if len(coded_provider_data) == 0 and provider != '':

        provider_data, browser = scrapeProviderData(browser, provider, provider_data)

    app_data, ratings, browser = scrapeAppData(browser, url, provider, featured_urls, category, rank, app_data)

    if ratings > 0:

        review_tab_button = browser.find_element_by_id('tab-default-2__item')
        browser.execute_script("arguments[0].scrollIntoView();", review_tab_button)
        review_tab_button.click()
        time.sleep(10)
        
        try:
            review_section = browser.find_element_by_id('appxRevsContainer')
        except selenium.common.exceptions.NoSuchElementException:
            try:
                time.sleep(60)
                review_section = browser.find_element_by_id('appxRevsContainer')
            except selenium.common.exceptions.TimeoutException:
                attempts = 0
                review_section = ''
                while attempts < 5 and provider == '':
                    browser.execute_script("arguments[0].scrollIntoView();", review_tab_button)
                    review_tab_button.click()
                    time.sleep(10)
                    try:
                        review_section = browser.find_element_by_id('appxRevsContainer')
                    except selenium.common.exceptions.NoSuchElementException:
                        attempts = attempts + 1

        if review_section != '':

            review_data = scrapeReviewData(browser, url, ratings, review_data)

    return app_data, provider_data, review_data

def scrapeReviewData(browser, url, ratings, review_data):

    focal_review_data = []
    print(ratings)

    while len(focal_review_data) < ratings and len(focal_review_data) < 2000:

        reviews = browser.find_elements_by_class_name('appx-review')

        for review in reviews:

            id = review.get_attribute('data-revid')

            coded_reviews = [r for r in focal_review_data if r['id'] == id]

            if len(coded_reviews) == 0:

                review_data_dict = {}

                review_data_dict['id'] = id
                review_data_dict['app_url'] = url
                review_data_dict['user'] = review.find_element_by_class_name('appx-review-user-detail').find_element_by_tag_name('a').get_attribute('href').split('profile?u=')[-1]
                review_data_dict['rating'] = review.find_element_by_class_name('appx-rating-block').find_element_by_tag_name('span').get_attribute('class')[-2]
                review_data_dict['date'] = review.find_element_by_class_name('appx-review-user-review').find_element_by_tag_name('a').text

                review_content = review.find_element_by_class_name('appx-review-content')
                review_paragraphs = review_content.find_elements_by_tag_name('p')

                review_data_dict['title'] = review_paragraphs[0].text
                review_data_dict['content'] = review_paragraphs[1].text

                focal_review_data.append(review_data_dict)

        print(len(focal_review_data))

        if len(focal_review_data) < ratings:

            browser.find_element_by_tag_name('body').send_keys(Keys.END)

            time.sleep(10)

            browser.find_element_by_id('appx_load_more_button').click()
    
            time.sleep(10)

    review_data = review_data + focal_review_data

    return review_data

def scrapeProviderData(browser, provider_name, provider_data):

    provider_data_dict = {}

    provider_data_dict['provider_name'] = provider_name

    try:
        provider_data_dict['location'] = browser.find_element_by_id('AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id321').text
    except selenium.common.exceptions.NoSuchElementException:
        provider_data_dict['location'] = ''
    try:
        provider_data_dict['founded'] = browser.find_element_by_id('AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id326').text.replace('Founded\n','')
    except selenium.common.exceptions.NoSuchElementException:
        provider_data_dict['founded'] = ''
    try:
        provider_data_dict['website'] = browser.find_element_by_id('AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id330').text.replace('Website\n','')
    except selenium.common.exceptions.NoSuchElementException:
        provider_data_dict['website'] = ''
    try:
        provider_data_dict['email'] = browser.find_element_by_id('AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id332').text.replace('Email\n','')
    except selenium.common.exceptions.NoSuchElementException:
        provider_data_dict['email'] = ''
    try:
        description_elements = browser.find_elements_by_class_name('appx-extended-detail-company-description')
        description = ''
        for description_element in description_elements:
            if description == '':
                description = description_element.text
            else:
                description = description + '\n' + description_element.text
        provider_data_dict['description'] = description
    except selenium.common.exceptions.NoSuchElementException:
        provider_data_dict['description'] = ''

    provider_data.append(provider_data_dict)

    return provider_data, browser

def scrapeAppData(browser, url, provider, featured_urls, category, rank, app_data):

    app_data_dict = {}

    app_data_dict['url'] = url
    app_data_dict['main_category'] = category
    app_data_dict['id'] = url.split("appxListingDetail?listingId=")[-1]
    app_data_dict['rank'] = rank
    app_data_dict['provider'] = provider

    if url in featured_urls:
        app_data_dict['featured'] = 1
    else:
        app_data_dict['featured'] = 0

    app_data_dict['title'] = browser.find_element_by_class_name('appx-page-header-2_title').text
    app_data_dict['pricing'] = browser.find_element_by_class_name('appx-pricing-detail-header').text
    app_data_dict['number_of_ratings'] = int(browser.find_element_by_class_name('appx-rating-amount').text.replace('(', '').replace(')', ''))
    if app_data_dict['number_of_ratings'] > 0:
        app_data_dict['rating'] = browser.find_element_by_id('appxListingDetailPageId:AppxLayout:j_id715:j_id716:j_id719').get_attribute('class')[:-2]
    else:
        app_data_dict['rating'] = 0
    app_data_dict['release_date'] = browser.find_element_by_class_name('appx-detail-section-first-listed').text.replace('LISTED ON\n', '')
    category_url = browser.find_element_by_id('appxListingDetailPageId:AppxLayout:listingCategories:0:firstCat')
    app_data_dict['category'] = category_url.find_element_by_tag_name('strong').text

    try:
        app_data_dict['tagline'] = browser.find_element_by_class_name('appx-headline-details-tagline').text
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['tagline'] = ''

    try:
        latest_release = browser.find_element_by_class_name('appx-detail-section-last-update')
        app_data_dict['latest_release'] = latest_release.text.replace('LATEST RELEASE\n', '')
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['latest_release'] = ''
 
    try:
        top_buttons = [e.text for e in browser.find_elements_by_class_name('appx-hide-s')]
        demo_button = [b for b in top_buttons if 'Demo' in b]
        testdrive_button = [b for b in top_buttons if 'Test' in b]
        if len(demo_button) > 0:
            app_data_dict['demo'] = 1
        else:
            app_data_dict['demo'] = 0
        
        if len(testdrive_button) > 0:
            app_data_dict['testdrive'] = 1
        else:
            app_data_dict['testdrive'] = 0
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['demo'] = 0
        app_data_dict['testdrive'] = 0

    try:
        browser.find_element_by_class_name('slds-button slds-button_brand appx-btn appx-btn-testdrive')
        app_data_dict['testdrive'] = 1
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['testdrive'] = 0
    
    try:
        description_elements = browser.find_elements_by_class_name('appx-extended-detail-subsection-paragraph')
        description = ''
        for description_element in description_elements:
            if description == '':
                description = description_element.text
            else:
                description = description + '\n' + description_element.text 
        app_data_dict['description'] = description
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['description'] = ''

    try:
        highlight_list_items = browser.find_element_by_id('AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id108').find_elements_by_tag_name('li')
        app_data_dict['highlights'] = ', '.join([e.text for e in highlight_list_items])
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['highlights'] = ''

    try:
        custom_objects = browser.find_element_by_id('AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id122:0')
        app_data_dict['number_of_custom_objects'] = custom_objects.text.replace('Custom Objects: ', '')
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['number_of_custom_objects'] = 0
    try:
        custom_apps = browser.find_element_by_id('AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id122:1')
        app_data_dict['number_of_custom_apps'] = custom_apps.text.replace('Custom Applications:', '')
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['number_of_custom_apps'] = 0
    try:
        custom_tabs = browser.find_element_by_id('AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id122:2')
        app_data_dict['number_of_custom_tabs'] = custom_tabs.text.replace('Custom Tabs: ', '')
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['number_of_custom_tabs'] = 0
    try:
        global_components = browser.find_element_by_id('AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id131:0')
        app_data_dict['number_of_global_components'] = global_components.text.replace('Global: ', '')
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['number_of_global_components'] = 0    
    try:
        app_builder_components = browser.find_element_by_id('AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id131:1')
        app_data_dict['number_of_app_builder_components'] = app_builder_components.text.replace('App Builder: ', '')
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['number_of_app_builder_components'] = 0    
    try:
        community_builder_components = browser.find_element_by_id('AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id131:2')
        app_data_dict['number_of_community_builder_components'] = community_builder_components.text.replace('Community Builder: ', '')
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['number_of_community_builder_components'] = 0    
    
    try:
        salesforce_editions = browser.find_element_by_class_name('appx-extended-detail-subsection-description')
        salesforce_edition_elements = salesforce_editions.find_elements_by_tag_name('a')
        salesforce_editions_list = [s.text for s in salesforce_edition_elements]
        app_data_dict['salesforce_editions'] = ' '.join(salesforce_editions_list)
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['salesforce_editions'] = ''

    try:
        app_data_dict['other_system_requirements'] = browser.find_element_by_id('AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id142').text.replace('Other System Requirements','')
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['additional_requirements'] = ''

    try:
        app_data_dict['app_version'] = browser.find_element_by_id('AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id181').text
    except selenium.common.exceptions.NoSuchElementException:
        app_data_dict['app_version'] = '1.0'

    ratings = app_data_dict['number_of_ratings']

    app_data.append(app_data_dict)

    return app_data, ratings, browser

if __name__ == '__main__':

    geckodriver = 'C:/Users/f-appstore/Downloads/geckodriver.exe'
    #geckodriver = '/Users/joeyvanangeren/downloads/geckodriver'
    options = webdriver.FirefoxOptions()
    #options.add_argument('-headless')

    browser = webdriver.Firefox(executable_path=geckodriver, options=options)

    category_urls = [('Sales', 'https://appexchange.salesforce.com/category/sales'), ('Customer Service', 'https://appexchange.salesforce.com/category/service'), ('Marketing', 'https://appexchange.salesforce.com/category/marketing'), ('IT & Administration', 'https://appexchange.salesforce.com/category/it-admin'), ('Human Resources', 'https://appexchange.salesforce.com/category/hr'), ('Finance', 'https://appexchange.salesforce.com/category/finance'), ('Enterprise Resource Planning', 'https://appexchange.salesforce.com/category/erp'), ('Collaboration', 'https://appexchange.salesforce.com/category/collaboration'), ('Analytics', 'https://appexchange.salesforce.com/category/analytics')]

    app_data = []
    provider_data = []
    review_data = []
    
    first_pageload = True
    
    for category, url in category_urls:

        print(category)

        app_urls, featured_urls = scrapeAppListingURLs(url, browser, first_pageload)
        
        first_pageload = False
        
        rank = 1

        for app_url in app_urls:

            print(app_url)

            app_data, provider_data, review_data = scrapeAppListingPage(app_url, browser, featured_urls, category, rank, app_data, provider_data, review_data)

            rank = rank + 1

    browser.quit()
            
    app_data_keys = app_data[0].keys()
    provider_data_keys = provider_data[0].keys()
    review_data_keys = review_data[0].keys()

    with open('appexchange_app_data_' + datetime.datetime.now().date().isoformat() + '.csv', 'wb') as app_data_file:
        dict_writer = csv.DictWriter(app_data_file, app_data_keys)
        dict_writer.writeheader()
        dict_writer.writerows(app_data)

    with open('appexchange_provider_data_' + datetime.datetime.now().date().isoformat() + '.csv', 'wb') as provider_data_file:
        dict_writer = csv.DictWriter(provider_data_file, provider_data_keys)
        dict_writer.writeheader()
        dict_writer.writerows(provider_data)

    with open('appexchange_review_data_' + datetime.datetime.now().date().isoformat() + '.csv', 'wb') as review_data_file:
        dict_writer = csv.DictWriter(review_data_file, review_data_keys)
        dict_writer.writeheader()
        dict_writer.writerows(review_data)