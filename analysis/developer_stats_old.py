import glob
import utils
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


path = "/Users/ajaysingh/Downloads/OldData/"
salesforce_developers = ['Salesforce Labs', 'salesforce.com', 'Salesforce.com Foundation']

all_files = glob.glob("/Users/ajaysingh/Downloads/OldData/*.csv")
developer_list = utils.getDeveloperDataFiles(all_files, 'App AppExchange Data')
final_list = utils.sortDeveloperFileNamesByDate(developer_list)
overall_stats = []

for meta in final_list:
    data = pd.read_csv(filepath_or_buffer=meta['filename'], sep=",", error_bad_lines=False)
    provider_frequency_map = data['Provider Name'].value_counts()
    paid_frequency_map = data['App Pricing'].value_counts()
    categories_frequency_map = data['App Categories'].value_counts()
    number_of_categories = len(categories_frequency_map.keys())
    number_of_apps = data.shape[0]
    salesforce_count = 0
    columns = ['No. of Custom Objects', 'No. of Custom Tabs', 'No. of Custom Apps']
    corr_data = pd.DataFrame(columns=columns)
    try:
        corr_data['No. of Custom Objects'] = data['No. of Custom Objects']
        corr_data['No. of Custom Tabs'] = data['No. of Custom Tabs']
        corr_data['No. of Custom Apps'] = data['No. of Custom Apps']
        print(corr_data.corr())
        import matplotlib.pyplot as plt
        plt.matshow(corr_data.corr())
        plt.show()
        break
    except KeyError as e:
        print(e)
        continue
    for key in salesforce_developers:
        salesforce_count+= provider_frequency_map[key]
    unique_providers_number = len(data['Provider Name'].unique())
    salesforce_fraction = float(salesforce_count/unique_providers_number)
    entry = {'date': meta['date'],
             'salesforce_fraction': salesforce_fraction,
             'unique_providers_number': unique_providers_number,
             'paid_app_fraction': float(paid_frequency_map['Free']/number_of_apps),
             'number_of_apps': number_of_apps,
             'number_of_categories': number_of_categories}
    overall_stats.append(entry)



# # Plot fraction of salesforce developed apps in overall total apps over the period of time
# X = np.array([entry['date'] for entry in provider_info])
# Y = np.array([entry['salesforce_fraction'] for entry in provider_info])
#
# plt.plot(X, Y)
# plt.show()
#
# # Plot the overall number of unique providers over the period of time
# X = np.array([entry['date'] for entry in provider_info])
# Y = np.array([entry['unique_providers_number'] for entry in provider_info])
#
# plt.plot(X, Y)
# plt.show()
#
# # Plot the fraction of paid_apps over the period of time
# X = np.array([entry['date'] for entry in provider_info])
# Y = np.array([entry['paid_app_fraction'] for entry in provider_info])
#
# plt.plot(X, Y)
# plt.show()
#
# # Plot the overall number of apps over the period of time
# X = np.array([entry['date'] for entry in provider_info])
# Y = np.array([entry['number_of_apps'] for entry in provider_info])
#
# plt.plot(X, Y)
# plt.show()
#
# # Plot the overall number of apps over the period of time
# X = np.array([entry['date'] for entry in provider_info])
# Y = np.array([entry['number_of_categories'] for entry in provider_info])
#
# plt.plot(X, Y)
# plt.show()




