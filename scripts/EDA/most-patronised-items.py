'''
    This is a comprehensive analysis on a transactional data from
    01/12/2010 to 09/12/2011, for a UK-based online retail store
'''

import pandas as pd
import matplotlib.pyplot as plt

# load data
df = pd.read_csv('../../data/processed/cleaned-data.csv')

# monthly trend of most patronised products (first five)
item_patronage = df.groupby('Description')['Quantity'].sum().nlargest(5)
item_patronage_df = df[df['Description'].isin(item_patronage.index)]
item_patronage_trend = item_patronage_df.groupby(['InvoiceMonth', 'Description'])['Quantity'].sum().unstack()

item_patronage_trend.plot(marker='o', ms=4)
plt.title('Monthly Trend of Most Patronised Products (first five)')
plt.tight_layout()
plt.savefig('../../figures/EDA/most-patronised-items.jpg')


