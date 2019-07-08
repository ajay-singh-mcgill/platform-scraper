import bleach
import re
import os

def parse_app_details(soup):
    meta_raw = soup.find('div', attrs= {'class': 'metaDetails'})
    products_raw = soup.find('div', attrs={'class':'cell products'})
    publisher_raw = soup.find('div', attrs={'itemprop':'publisher'})
    version_raw = soup.find('div', attrs={'itemprop': 'version'})
    date_updated_raw = soup.find('div', attrs= {'itemprop': 'dateModified'})
    categories_raw = soup.find('div', attrs={'class': 'cell categoriesSupported'})
    app_header_raw  = soup.find('h1', attrs={'class': 'c-heading-4 titleHeader ampTitleHeader'})
    rating_raw = soup.find('div', attrs={'class': 'AMPappRatingcell'})
    description_heading_raw = soup.find('h2', attrs={'itemprop': 'description'})
    description_raw = soup.find('div', attrs={'class': 'description'})
    add_in_capabilities_raw = soup.find('div', attrs={'class': 'capabilities'})
    final_acquire_using = []
    acquire_using = re.findall('Acquire Using(.*)version', str(meta_raw))
    if acquire_using:
        acquire_using = acquire_using[0]
        for entry in acquire_using.split("<span>")[1:]:
            final_acquire_using.append(entry.split("</span>")[0])
    final_products = []
    products = re.findall('title=\"(.*)\">', str(products_raw))
    for prod in products:
        if prod.split("\"")[0]:
            final_products.append(prod.split("\"")[0])
    publisher = re.findall('itemprop=\"name\">(.*)</span>', str(publisher_raw))
    if publisher:
        publisher = publisher[0]
    else:
        publisher = "NA"
    version = re.findall('Version</h2><span>(.*)</span>', str(version_raw))
    if version:
        version = version[0]
    else:
        version = "NA"
    updated_on  = re.findall('Updated</h2><span>(.*)</span>', str(date_updated_raw))
    if updated_on:
        updated_on = updated_on[0]
    else:
        updated_on = "NA"
    final_categories = []
    if categories_raw:
        categories = str(categories_raw).split("title=")
    else:
        categories = None
    if categories:
        for cat in categories[1:]:
            final_categories.append(cat.split(">")[0].strip("\""))
    heading = re.findall('itemprop="name">(.*)</h1>', str(app_header_raw))[0]
    review_count = re.findall('-->(.*)<!--', str(rating_raw))
    if review_count:
        review_count = review_count[0]
    else:
        review_count = "NA"
    rating = re.findall('<span>(.*)</span>', str(rating_raw))
    if rating:
        rating = rating[0]
    else:
        rating = "NA"
    short_description = re.findall('itemprop=\"description\">(.*)</h2>', str(description_heading_raw))
    if short_description:
        short_description = short_description[0]
    else: short_description= "NA"
    description = bleach.clean(str(description_raw), strip=True, strip_comments=True)
    add_in_capabilities = bleach.clean(str(add_in_capabilities_raw), strip=True, strip_comments=True)
    print("\n".join([str(final_products), str(final_categories), publisher, version, updated_on, heading, review_count, rating,
                     short_description, description, add_in_capabilities, str(final_acquire_using)]))
    print("\n\n\n\n\n\n")










