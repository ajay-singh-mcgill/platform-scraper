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


def plot_correlation_matrix(df):
    corr_data = pd.DataFrame(columns=columns)
    try:
        corr_data['No. of Custom Objects'] = df['No. of Custom Objects']
        corr_data['No. of Custom Tabs'] = df['No. of Custom Tabs']
        corr_data['No. of Custom Apps'] = df['No. of Custom Apps']
        print(corr_data.corr())
        import matplotlib.pyplot as plt
        plt.matshow(corr_data.corr())
        plt.show()
    except KeyError as e:
        print(e)

def classify_developers(data):
    total_number_of_reviews = data['Number of Reviews'].sum()
    print(total_number_of_reviews)
    provider_frequency_map = data['Provider Name'].value_counts()
    print(provider_frequency_map)
    # for provider in provider_frequency_map.keys():
    #     print(provider)
    #     provider_app_data = data.loc[data['Provider Name'] == provider]

for meta in final_list:
    print(meta['filename'])
    data = pd.read_csv(filepath_or_buffer=meta['filename'], sep=",", error_bad_lines=False)
    provider_frequency_map = data['Provider Name'].value_counts()
    paid_frequency_map = data['App Pricing'].value_counts()
    categories_frequency_map = data['App Categories'].value_counts()
    classify_developers(data)
    break
    number_of_categories = len(categories_frequency_map.keys())
    number_of_apps = data.shape[0]
    salesforce_count = 0
    columns = ['No. of Custom Objects', 'No. of Custom Tabs', 'No. of Custom Apps']
    number_of_apps = data.shape[0]
    salesforce_count = 0
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



# Plot fraction of salesforce developed apps in overall total apps over the period of time
# X = np.array([entry['date'] for entry in overall_stats])
# Y = np.array([entry['salesforce_fraction'] for entry in overall_stats])
#
# plt.plot(X, Y)
# plt.show()
#
# # Plot the overall number of unique providers over the period of time
# X = np.array([entry['date'] for entry in overall_stats])
# Y = np.array([entry['unique_providers_number'] for entry in overall_stats])
#
# plt.plot(X, Y)
# plt.show()
#
# # Plot the fraction of paid_apps over the period of time
# X = np.array([entry['date'] for entry in overall_stats])
# Y = np.array([entry['paid_app_fraction'] for entry in overall_stats])
#
# plt.plot(X, Y)
# plt.show()
#
# # Plot the overall number of apps over the period of time
# X = np.array([entry['date'] for entry in overall_stats])
# Y = np.array([entry['number_of_apps'] for entry in overall_stats])
#
# plt.plot(X, Y)
# plt.show()
#
# # Plot the overall number of apps over the period of time
# X = np.array([entry['date'] for entry in overall_stats])
# Y = np.array([entry['number_of_categories'] for entry in overall_stats])
#
# plt.plot(X, Y)
# plt.show()




