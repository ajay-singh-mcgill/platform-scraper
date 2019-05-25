import bleach
import re

def parse_app_page_overview_tab(soup):
    print('Getting the overview tab details...........................\n\n\n\n\n')
    detailed_description_raw = str(soup.find('div', attrs={'class': 'appx-extended-detail-subsection'}))
    print(re.sub('<[^>]*>', '', bleach.clean(detailed_description_raw, strip=True, strip_comments=True)))
    highlights_raw = str(soup.find('div', attrs={'class': 'appx-feature-menu'}))
    print(re.sub('<[^>]*>', '', bleach.clean(highlights_raw, strip=True, strip_comments=True)))
    package_contents = str(soup.find('ul', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id122'}))
    print(re.sub('<[^>]*>', '', bleach.clean(package_contents, strip=True, strip_comments=True)))
    lightning_components = str(soup.find('ul', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id131'}))
    print(re.sub('<[^>]*>', '', bleach.clean(lightning_components, strip=True, strip_comments=True)))
    requirements = str(soup.find('span', attrs={'id': 'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id134'}))
    print(re.sub('<[^>]*>', '', bleach.clean(requirements, strip=True, strip_comments=True)))
    version = str(soup.find('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id181'}))
    print(re.sub('<[^>]*>', '', bleach.clean(version, strip=True, strip_comments=True)))
    first_release=str(soup.find('div', attrs={'id':'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id184'}))
    print(re.sub('<[^>]*>', '', bleach.clean(first_release, strip=True, strip_comments=True)))
    latest_release= str(soup.find('div', attrs={'id': 'AppxListingDetailOverviewTab:listingDetailOverviewTab:appxListingDetailOverviewTabComp:j_id186'}))
    print(re.sub('<[^>]*>', '', bleach.clean(latest_release, strip=True, strip_comments=True)))
    languages = str(soup.find('a', attrs={'data-events':'listing-languages'}))
    print(re.sub('<[^>]*>', '', bleach.clean(languages, strip=True, strip_comments=True)))
    line_entry = ",".join(['app_overview_details'])
    return line_entry

def parse_reviews_data(soup):
    print(soup)

def parse_app_page_data(soup):
    price_raw = str(soup.find('p', {'class': 'appx-pricing-detail-header'}))
    price = re.search('j_id693\">(.*)</span>', price_raw)
    if price is None:
        price = re.search('planCharges\">(.*)</span>', price_raw)
    price = price.group(1)
    price = re.sub('<[^>]*>', '', price)
    number_of_reviews_raw = str(soup.find('span', attrs={'id': 'appxListingDetailPageId:AppxLayout:j_id715:j_id716:j_id723'}))
    number_of_reviews = re.search('j_id723\">(.*)</span>', number_of_reviews_raw).group(1)
    review_stars_raw = str(soup.find('span', attrs={'id':'appxListingDetailPageId:AppxLayout:j_id715:j_id716:j_id719'}))
    review_stars = re.search('appx-rating-stars-(.*)\" id', review_stars_raw)
    if review_stars is not None:
        review_stars = review_stars.group(1)
    listed_on_raw =  str(soup.find('div', attrs={'class': 'appx-detail-section-first-listed'}))
    listed_on = re.search('<p>(.*)</p>', listed_on_raw).group(1)
    latest_release_raw = str(soup.find('span', attrs={'id': 'appxListingDetailPageId:AppxLayout:j_id732'}))
    latest_release = re.search('<p>(.*)</p>', latest_release_raw).group(1)
    categories_raw = str(soup.find('div', attrs={'class': 'appx-headline-details-categories-details'}))
    categories = re.search('<strong>(.*)</strong>', categories_raw).group(1)
    descrition_raw = str(soup.find('div', attrs={'class':'appx-detail-section-description'}))
    description = re.search('<p>(.*)</p>', descrition_raw).group(1)
    line_entry = ",".join([str(price), str(number_of_reviews), str(review_stars), str(listed_on)
                              , str(latest_release), str(categories), str(description)])
    return line_entry

