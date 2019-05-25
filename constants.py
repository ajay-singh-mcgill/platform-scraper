category_url_dict = {
    'hr': 'https://appexchange.salesforce.com/category/hr',
    'marketing': 'https://appexchange.salesforce.com/category/marketing',
    'it_admin': 'https://appexchange.salesforce.com/category/it-admin',
    'erp': 'https://appexchange.salesforce.com/category/erp',
    'analytics': 'https://appexchange.salesforce.com/category/analytics',
    'collaboration': 'https://appexchange.salesforce.com/category/collaboration',
    'customer_service': 'https://appexchange.salesforce.com/category/service',
    'finance': 'https://appexchange.salesforce.com/category/finance'
}

page_load_wait_time = 5
category_page_show_more_button_id = 'appx-load-more-button-id'
category_page_app_matrix_id = 'appx-table-results'
app_overview_tab_base_url = 'https://appexchange.salesforce.com/AppxListingDetailOverviewTab?listingId='
output_file_header = "app_title, listing_id, url, price, number_of_reviews, review_stars, listed_on, " \
                     "latest_release, categories, description, detailed_description, highlights, custom_tabs, " \
                     "custom_objects, custom_applications, lightning_components_global,  " \
                     "lightning_components_community_builder, lightning_components_app_builder, salesforce_edition, " \
                     "other_system_requirements, version, first_release, languages \n"