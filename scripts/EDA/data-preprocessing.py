'''
    This is a comprehensive analysis on a transactional data from
    01/12/2010 to 09/12/2011, for a UK-based online retail store
'''

import pandas as pd
import matplotlib.pyplot as plt

# load data
df = pd.read_excel('../data/raw/online-retail.xlsx')

# get info about dataset
df.info()
df.describe()

''' Data Pre-processing '''

# drop duplicate data
df.drop_duplicates(inplace=True)

# drop rows with missing entries
df.dropna(inplace=True)

# convert timestamp column to Date data type
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# extract date component of the timestamp
df['Date'] = df['InvoiceDate'].dt.date

# extract year/month from date
df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')

# drop negative values
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# remove invoice numbers that start with C
df['InvoiceNo'] = df['InvoiceNo'].astype(str)
df = df[~df['InvoiceNo'].str.lower().str.startswith('c')]

# create a new column: total price of each item
df['TotalPrice'] = df['UnitPrice'] * df['Quantity']

# save cleaned data
df.to_csv('../data/processed/cleaned-data.csv')