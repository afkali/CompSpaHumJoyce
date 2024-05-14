import pandas as pd
import csv

df = pd.read_csv('NLP/try2.csv')

df['test']  = df['name'].str.len()

# df.dropna()

df['test'] = df['test'].astype('int')

# combine to tuples (because spacy wants tupels for whatever fkng reason)
df['loc_col'] = list(zip([0] * len(df), df.test, ['LOC'] * len(df)))


df = df[['name', 'loc_col']]

df.to_csv('NLP/may24.tsv', sep='\t', index=False)



# 0 * len(df) to have 0 for every single row of df
