'''
    This is a comprehensive analysis on a transactional data from
    01/12/2010 to 09/12/2011, for a UK-based online retail store
'''

import pandas as pd
import matplotlib.pyplot as plt

# load data
df = pd.read_csv('../../data/processed/cleaned-data.csv')

# invoice with the high returns (first five)
valuable_invoice = df.groupby('InvoiceNo')['TotalPrice'].sum().nlargest(5)

valuable_invoice.plot(kind='bar')
plt.xlabel('Invoice ID')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45, ha='right', va='top')
plt.title('5 Most Valuable Invoices')
plt.tight_layout()
plt.savefig('../../figures/EDA/valuable-invoices.jpg')
