import pandas as pd
import matplotlib.pyplot as plt

filepath = "../data/2019-06-09 13:01:00.812428.csv"
apps_df = pd.read_csv(filepath_or_buffer=filepath, sep="~", error_bad_lines=False)

print(apps_df[' developer_name'].value_counts())



