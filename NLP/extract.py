# script to extract only relevant rows from huge keggle dataset

import pandas as pd

df = pd.read_csv("NLP/geonames.csv")

# print(df.head)


ie_df = df[df['country code'] == 'IE']

columns = ['name', 'country code']

final_df = ie_df[columns]

unique_df = final_df.drop_duplicates(subset=['name'])

unique_df.to_csv('NLP/try2.csv', index=False)