category_url_dict = {
    'hr': 'https://appexchange.salesforce.com/category/hr',
    'marketing': 'https://appexchange.salesforce.com/category/marketing',
    'it_admin': 'https://appexchange.salesforce.com/category/it-admin',
    'erp': 'https://appexchange.salesforce.com/category/erp',
    'analytics': 'https://appexchange.salesforce.com/category/analytics',
    'collaboration': 'https://appexchange.salesforce.com/category/collaboration',
    'customer_service': 'https://appexchange.salesforce.com/category/customer-service',
    'finance': 'https://appexchange.salesforce.com/category/finance',
    'sales': 'https://appexchange.salesforce.com/category/sales'
}

page_load_wait_time = 5
category_page_show_more_button_id = 'appx-load-more-button-id'
category_page_app_matrix_id = 'appx-table-results'
app_overview_tab_base_url = 'https://appexchange.salesforce.com/AppxListingDetailOverviewTab?listingId='
output_file_header = "app_title~ listing_id~ url~ price~ number_of_reviews~ review_stars~ listed_on~ " \
                     "latest_release~ categories~ description~ detailed_description~ highlights~ custom_tabs~ " \
                     "custom_objects~ custom_applications~ lightning_components_global~  " \
                     "lightning_components_community_builder~ lightning_components_app_builder~ salesforce_edition~ " \
                     "other_system_requirements~ version~ first_release~ languages~ " \
                     "developer_founded~ developer_website~ developer_email~ developer_phone~ developer_name~ " \
                     "developer_location~ developer_detail\n"

salesforce_review_data_file_header = "url~ app_id~ review_data\n"

# Dev Environment
#gecko_logpath = "/Users/ajaysingh/PycharmProjects/platform_scraper"
#executable_path = '/usr/local/bin/geckodriver'
#data_folder_path = "/Users/ajaysingh/PycharmProjects/platform_scraper/data/"
#microsoft_data_folder_path = "/Users/ajaysingh/PycharmProjects/platform_scraper/microsoft_data/"
#salesforce_review_data_folder = "/Users/ajaysingh/PycharmProjects/platform_scraper/review_data/salesforce/"

#Prod Environment
gecko_logpath = "/home/crawler/appexchange"
executable_path = "/home/crawler/geckodriver"
data_folder_path = "/home/crawler/appexchange/data/"
microsoft_data_folder_path = "/home/crawler/appexchange/microsoft_data/"
salesforce_review_data_folder = "/home/crawler/appexchange/review_data/salesforce/"

microsoft_category_url_dict = {
    "analytics": "https://appsource.microsoft.com/en-us/marketplace/apps?category=analytics",
    "sales": "https://appsource.microsoft.com/en-us/marketplace/apps?category=sales",
    "productivity": "https://appsource.microsoft.com/en-us/marketplace/apps?category=productivity",
    "operations": "https://appsource.microsoft.com/en-us/marketplace/apps?category=operations",
    "marketing": "https://appsource.microsoft.com/en-us/marketplace/apps?category=marketing",
    "iot": "https://appsource.microsoft.com/en-us/marketplace/apps?category=iot",
    "finance": "https://appsource.microsoft.com/en-us/marketplace/apps?category=finance",
    "customer-service": "https://appsource.microsoft.com/en-us/marketplace/apps?category=customer-service",
    "it-admin": "https://appsource.microsoft.com/en-us/marketplace/apps?category=it-admin",
    "human-resources": "https://appsource.microsoft.com/en-us/marketplace/apps?category=human-resources",
    "collaboration": "https://appsource.microsoft.com/en-us/marketplace/apps?category=collaboration",
    "artifical-intelligence": "https://appsource.microsoft.com/en-us/marketplace/apps?category=artifical-intelligence",
}

microsoft_base_url = 'https://appsource.microsoft.com'
microsoft_app_price_url = 'https://appsource.microsoft.com/view/appPricing/us?version=2017-04-24'
microsoft_file_header= "~".join(['industries','products_affected', 'categories', 'publisher', 'version', 'updated_on', 'heading',
                                 'review_count', 'rating','short_description', 'description', 'add_in_capabilities',
                                 'acquire_using', 'url', 'app_id', "\n"])


