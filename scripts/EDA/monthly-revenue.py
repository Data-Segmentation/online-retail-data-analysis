'''
    This is a comprehensive analysis on a transactional data from
    01/12/2010 to 09/12/2011, for a UK-based online retail store
'''

import pandas as pd
import matplotlib.pyplot as plt

# load data
df = pd.read_csv('../../data/processed/cleaned-data.csv')

# monthly total revenue
monthly_revenue = df.groupby('InvoiceMonth')['TotalPrice'].sum()

monthly_revenue.plot(kind='bar')
plt.xlabel('Month of Year')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45, ha='right', va='top')
plt.title('Monthly Total Revenue')
plt.tight_layout()
plt.savefig('../../figures/EDA/monthly-revenue.jpg')

