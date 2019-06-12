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
provider_info = []

for meta in final_list:
    data = pd.read_csv(filepath_or_buffer=meta['filename'], sep=",", error_bad_lines=False)
    provider_frequency_map = data['Provider Name'].value_counts()
    paid_frequency_map = data['App Pricing'].value_counts()
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
             'number_of_apps': number_of_apps}
    provider_info.append(entry)


# Plot fraction of salesforce developed apps in overall total apps over the period of time
X = np.array([entry['date'] for entry in provider_info])
Y = np.array([entry['salesforce_fraction'] for entry in provider_info])

plt.plot(X, Y)
plt.show()

# Plot the overall number of unique providers over the period of time
X = np.array([entry['date'] for entry in provider_info])
Y = np.array([entry['unique_providers_number'] for entry in provider_info])

plt.plot(X, Y)
plt.show()

# Plot the overall number of unique providers over the period of time
X = np.array([entry['date'] for entry in provider_info])
Y = np.array([entry['paid_app_fraction'] for entry in provider_info])

plt.plot(X, Y)
plt.show()

# Plot the overall number of unique providers over the period of time
X = np.array([entry['date'] for entry in provider_info])
Y = np.array([entry['number_of_apps'] for entry in provider_info])

plt.plot(X, Y)
plt.show()




