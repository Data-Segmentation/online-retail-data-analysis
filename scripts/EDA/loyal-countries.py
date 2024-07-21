'''
    This is a comprehensive analysis on a transactional data from
    01/12/2010 to 09/12/2011, for a UK-based online retail store
'''

import pandas as pd
import matplotlib.pyplot as plt

# load data
df = pd.read_csv('../../data/processed/cleaned-data.csv')

# countries with high returns
loyal_countries = df.groupby('Country').agg({
    'Quantity': 'sum',
    'TotalPrice': 'sum'
}).nlargest(5, 'Quantity')

loyal_countries.plot(kind='bar')
plt.xlabel('Country')
plt.ylabel('Number of Items (Quantity) / Total Expenses')
plt.title('5 Most Loyal Countries and their Expenses')
plt.xticks(rotation=45, ha='right', va='top')
plt.tight_layout()
plt.savefig('../../figures/EDA/loyal-countries.jpg')

