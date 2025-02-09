import bleach
import re
import os

def get_highlights_list(data):
    output, counter = [], 1
    data = os.linesep.join([s for s in data.splitlines() if s])
    for d in data.split("\n"):
        if d.__len__() == 4:
            continue
        if counter%2==0:
            output.append(d)
        counter+=1
    return output

def get_developer_details(soup):
    developer_detail_raw = str(soup.find('p', attrs={'class':'appx-extended-detail-company-description'}))
    developer_founded_raw = str(soup.find('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id326'}))
    developer_website_raw = str(soup.find('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id330'}))
    developer_email_raw= str(soup.find('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id332'}))
    developer_phone_raw = str(soup.find('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id334'}))
    developer_name_raw = str(soup.find('div', attrs={'class':'appx-company-name'}))
    developer_location_raw = str(soup.find('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id321'}))

    try:
        developer_founded = developer_founded_raw.split('slds-truncate\">')[1].split("\n")[0]
    except IndexError as e:
        developer_founded = "NA"
    try:
        developer_website = developer_website_raw.split('_blank\">')[1].split("</a>")[0]
    except IndexError as e:
        developer_website = "NA"
    try:
        developer_email = developer_email_raw.split('mailto:')[1].split("\"")[0]
    except IndexError as e:
        developer_email = "NA"
    try:
        developer_phone = developer_phone_raw.split("appx-extended-detail-subsection-description\">")[1].split("\n")[0]
    except IndexError as e:
        developer_phone = "NA"
    try:
        developer_name = developer_name_raw.split("appx-company-name\">")[1].split("</div>")[0]
    except IndexError as e:
        developer_name = "NA"
    try:
        developer_location = developer_location_raw.split("appxListingDetailOverviewTabComp:j_id321\">")[1].split('</div>')[0]
    except IndexError as e:
        developer_location = "NA"
    try:
        developer_detail = str(re.sub('<[^>]*>', '', bleach.clean(developer_detail_raw, strip=True, strip_comments=True)))
    except IndexError as e:
        developer_detail = "NA"
    developer_detail_final = "~".join([developer_founded, developer_website, developer_email, developer_phone, developer_name,
                                       developer_location, developer_detail])
    developer_detail_final = developer_detail_final.replace("\n", "")
    return developer_detail_final

def parse_app_page_overview_tab(soup):
    detailed_description_raw = str(soup.find('div', attrs={'class': 'appx-extended-detail-subsection'}))
    if detailed_description_raw:
        detailed_description = re.sub('<[^>]*>', '', bleach.clean(detailed_description_raw, strip=True, strip_comments=True))
        detailed_description = re.sub("\n|\r|\t", "", detailed_description)
    else: detailed_description = ""
    highlights_raw = str(soup.find('div', attrs={'class': 'appx-feature-menu'}))
    if(highlights_raw):
        highlights = re.sub('<[^>]*>', '', bleach.clean(highlights_raw, strip=True, strip_comments=True))
        highlights = str(get_highlights_list(highlights))
    package_contents_raw = str(soup.find('ul', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id122'}))
    package_contents = re.sub('<[^>]*>', '', bleach.clean(package_contents_raw, strip=True, strip_comments=True))
    try:
        custom_objects = package_contents.split("Custom Objects:")[1].split("\n")[0]
    except IndexError as e:
        custom_objects = 'NA'
    try:
        custom_applications = package_contents.split("Custom Applications:")[1].split("\n")[0]
    except IndexError as e:
        custom_applications = 'NA'
    try:
        custom_tabs = package_contents.split("Custom Tabs:")[1].split("\n")[0]
    except IndexError as e:
        custom_tabs = 'NA'
    lightning_components_raw = str(soup.find('ul', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id131'}))
    lightning_components = re.sub('<[^>]*>', '', bleach.clean(lightning_components_raw, strip=True, strip_comments=True))
    try:
        lightning_components_global = lightning_components.split("Global:")[1].split("\n")[0]
    except IndexError as e:
        lightning_components_global = 'NA'
    try:
        lightning_components_app_builder = lightning_components.split("App Builder:")[1].split("\n")[0]
    except IndexError as e:
        lightning_components_app_builder = 'NA'
    try:
        lightning_components_community_builder = lightning_components.split("Community Builder:")[1].split("\n")[0]
    except IndexError as e:
        lightning_components_community_builder = 'NA'
    requirements_raw = str(soup.find('span', attrs={'id': 'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id134'}))
    requirements = re.sub('<[^>]*>', '', bleach.clean(requirements_raw, strip=True, strip_comments=True))
    try:
        salesforce_edition = requirements.split("Salesforce Edition")[1].split("Other System Requirements")[0].replace("\n", "").replace(" ", "")
    except IndexError as e:
        salesforce_edition = 'NA'
    try:
        other_system_requirements = requirements.split("Other System Requirements")[1].split("\n")[1]
    except IndexError as e:
        other_system_requirements = 'NA'
    version_raw = str(soup.find('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id181'}))
    version = re.sub('<[^>]*>', '', bleach.clean(version_raw, strip=True, strip_comments=True)).strip()
    first_release_raw =str(soup.find('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id184'}))
    first_release = re.sub('<[^>]*>', '', bleach.clean(first_release_raw, strip=True, strip_comments=True))
    try:
        first_release = first_release.split("First Release")[1].split("\n")[1]
    except IndexError as e:
        first_release = 'NA'
    languages_raw = soup.find_all('a', attrs={'data-event':'listing-languages'})
    languages = []
    for lan_data in languages_raw:
        try:
            language = bleach.clean(str(lan_data), strip=True, strip_comments=True)
            language = re.sub('<[^>]*>', '', language).replace("\n", '').replace(" ", "").replace(",", '')
            languages.append(language)
        except IndexError as e:
            continue

    developer_details = get_developer_details(soup)

    return "~".join([detailed_description, highlights, custom_tabs, custom_objects, custom_applications, lightning_components_global,
                     lightning_components_community_builder, lightning_components_app_builder, salesforce_edition, other_system_requirements,
                     version, first_release, str(languages), developer_details])

def parse_reviews_data(soup):
    print(soup)

def parse_app_page_data(soup):
    price_raw = str(soup.find('p', {'class': 'appx-pricing-detail-header'}))
    price = re.search('j_id693\">(.*)</span>', price_raw)
    if price is None:
        price = re.search('planCharges\">(.*)</span>', price_raw)
    if price:
        price = price.group(1)
        price = re.sub('<[^>]*>', '', price)
    else:
        price = 'NA'
    number_of_reviews_raw = str(soup.find('span', attrs={'id': 'appxListingDetailPageId:AppxLayout:j_id715:j_id716:j_id723'}))
    no_of_reviews = re.search('j_id723\">(.*)</span>', number_of_reviews_raw)
    if no_of_reviews:
        number_of_reviews = re.search('j_id723\">(.*)</span>', number_of_reviews_raw).group(1)
    else:
        number_of_reviews = '0'
    review_stars_raw = str(soup.find('span', attrs={'id':'appxListingDetailPageId:AppxLayout:j_id715:j_id716:j_id719'}))
    review_stars = re.search('appx-rating-stars-(.*)\" id', review_stars_raw)
    if review_stars is not None:
        review_stars = review_stars.group(1)
    listed_on_raw =  str(soup.find('div', attrs={'class': 'appx-detail-section-first-listed'}))
    listed_on_date = re.search('<p>(.*)</p>', listed_on_raw)
    if listed_on_date:
        listed_on = re.search('<p>(.*)</p>', listed_on_raw).group(1)
    else:
        listed_on = 'NA'
    latest_release_raw = str(soup.find('span', attrs={'id': 'appxListingDetailPageId:AppxLayout:j_id732'}))
    latest_rel = re.search('<p>(.*)</p>', latest_release_raw)
    if latest_rel:
        latest_release = latest_rel.group(1)
    else:
        latest_release = ""
    categories_raw = str(soup.find('div', attrs={'class': 'appx-headline-details-categories-details'}))
    categories = re.search('<strong>(.*)</strong>', categories_raw).group(1)
    descrition_raw = str(soup.find('div', attrs={'class':'appx-detail-section-description'}))
    description = re.search('<p>(.*)</p>', descrition_raw).group(1)
    line_entry = "~".join([str(price), str(number_of_reviews), str(review_stars), str(listed_on)
                              , str(latest_release), str(categories), str(description)])
    return line_entry

