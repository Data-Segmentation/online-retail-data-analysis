'''
    This is a comprehensive analysis on a transactional data from
    01/12/2010 to 09/12/2011, for a UK-based online retail store
'''

import pandas as pd
import matplotlib.pyplot as plt

# load data
df = pd.read_csv('../../data/processed/cleaned-data.csv')

#   most loyal customers
loyal_customer =df.groupby('CustomerID').agg({
    'Quantity': 'sum',
    'TotalPrice': 'sum'
}).nlargest(10, 'Quantity')

loyal_customer.plot(kind='bar')
plt.xlabel('Customer ID')
plt.ylabel('Number of Purchases/Total Expenses')
plt.title('10 Most Loyal Customers and their Expenses')
plt.xticks(rotation=45, ha='right', va='top')
plt.tight_layout()
plt.savefig('../../figures/EDA/loyal-customers.jpg')
