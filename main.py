'''
    This is a comprehensive analysis on a transactional data from
    01/12/2010 to 09/12/2011, for a UK-based online retail store
    This is the main program - there are other modules
'''

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('online-retail.xlsx')

#   get info about dataset
df.info()
df.describe()

# import modules
import customer_clusters
import customer_retention
import customer_life_value
import daily_purchase_trend
import customer_patronage_forecast


'''  clean data   '''
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# drop negative values
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# remove invoice numbers that start with C
df['InvoiceNo'] = df['InvoiceNo'].astype(str)
df = df[~df['InvoiceNo'].str.lower().str.startswith('c')]

# extract date component of the timestamp
df['Date'] = df['InvoiceDate'].dt.date

# extract year/month from date
df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')

# total price of each item
df['TotalPrice'] = df['UnitPrice'] * df['Quantity']

'''  analyse data   '''
#   Items that yield high returns (first ten)
item_value = df.groupby('Description')['TotalPrice'].sum().nlargest(10)
item_value.to_excel('output data/most-valuable-items.xlsx')

#   countries with high patronage (first ten)
top_countries = df['Country'].value_counts().nlargest(10)
top_countries.to_excel('output data/top-patronage-countries.xlsx')

#   monetary returns of countries
value_country = df.groupby('Country')['TotalPrice'].sum().nlargest(10)
value_country.to_excel('output data/most-valuable-countries.xlsx')

#   invoice with the high returns (first ten)
top_buy = df.groupby('InvoiceNo')['TotalPrice'].sum().nlargest(10)
top_buy.to_excel('output data/valuable-transactions.xlsx')


#   monthly total revenue
df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')
df['TotalPrice'] = df['UnitPrice'] * df['Quantity']
monthly_revenue = df.groupby('InvoiceMonth')['TotalPrice'].sum()
monthly_revenue.to_excel('output data/monthly-revenue.xlsx')
'''
plt.plot(monthly_revenue.index.astype(str), monthly_revenue.values, marker='o')
plt.xlabel('Month of Year')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45, ha='right', va='top')
plt.title('Monthly Total Revenue')
plt.tight_layout()
plt.savefig('output figures/monthly-revenue.jpg')
plt.show()
'''

#   monthly trend of most patronised products (first five)
df['Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
item_patronage = df.groupby('Description')['Quantity'].sum().nlargest(5)
item_patronage_df = df[df['Description'].isin(item_patronage.index)]
item_patronage_trend = item_patronage_df.groupby(['Month', 'Description'])['Quantity'].sum().unstack()
item_patronage_trend.plot(marker='o', ms=4)
print(item_patronage)
plt.tight_layout()
plt.title('Monthly Trend of Most Patronised Products (first five)')
plt.savefig('output figures/most-patronised-items.jpg')
plt.tight_layout()
plt.show()

#   most loyal customers
loyal_customer =df.groupby('CustomerID').agg({
    'Quantity': 'sum',
    'TotalPrice': 'sum'
}).nlargest(10, 'Quantity')
loyal_customer.plot(kind='bar')
plt.xlabel('Customer')
plt.ylabel('Number of Purchases/Total Expenses')
plt.title('10 Most Loyal Customers and their Expenses')
plt.xticks(rotation=45, ha='right', va='top')
plt.tight_layout()  # fit everything within the figure
plt.savefig('output figures/loyal-customers.jpg')
plt.show()




'''
                *** This part of the code is NOT tested ***
it's supposed to determined items purchased together (my laptop needs a bigger RAM); 8GiB isn't enough :)


from mlxtend.frequent_patterns import apriori, association_rules
from scipy.sparse import csr_matrix

basket = df.groupby(['InvoiceNo', 'Description'])['Quantity'].sum().unstack()

#   convert basket values to binary
def encode_unit(x):
    return 1 if x >= 1 else 0

basket_set = basket.applymap(encode_unit)

basket_sparse = csr_matrix(basket_set.values)

#   apply algorithm and generate rules
frequent_itemset = apriori(pd.DataFrame.sparse.from_spmatrix(basket_sparse, columns=basket_set.columns), min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemset, metric='lift', min_threshold=1)
rules = rules[rules['lift'] >= 6]

print(rules.head(10))
'''