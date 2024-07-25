# Exploratory Data Analysis

This project focuses on analyzing online retail sales data to derive insights and trends. The analysis is performed using 
Python with the help of `pandas`, `matplotlib`, and `seaborn` libraries. This document provides an overview of the code and 
its functionality for data processing and exploratory analysis.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Code Overview](#code-overview)
   - [Data Loading](#data-loading)
   - [Data Pre-processing](#data-pre-processing)
   - [Data Analysis](#data-analysis)
   - [Visualization](#visualization)
3. [Conclusion](#conclusion)


## Prerequisites

Ensure you have the following libraries installed:

```bash
pip install pandas matplotlib seaborn
```

## Code Overview

The script performs data loading, cleaning, processing, and various analytical tasks on the online retail dataset.

### Data Loading

The dataset is loaded from an Excel file located at `../data/online-retail.xlsx`. The initial data exploration 
includes viewing the dataset's information and statistical summary. This helps in understanding the structure and basic 
statistics of the dataset.

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_excel('../data/online-retail.xlsx')

# Get info about dataset
df.info()
df.describe()
```

### Data Pre-processing

The pre-processing steps include cleaning the data by removing duplicates, handling missing values, converting date 
formats, and filtering invalid entries. These steps are crucial for ensuring the data quality and reliability of the 
analysis results.

1. **Removing Duplicates and Missing Entries:**
    - **Drop duplicate rows:** Duplicate entries can skew the analysis, so they are removed.
    - **Drop rows with any missing values:** Missing values can lead to inaccurate calculations, so they are removed.

2. **Date and Time Handling:**
    - **Convert the `InvoiceDate` column to datetime format:** This allows for easier manipulation and extraction of date-related features.
    - **Extract the date and month from the `InvoiceDate` column:** These features are useful for time-based analysis.

3. **Filtering Data:**
    - **Remove rows with negative `Quantity` or `UnitPrice` values:** Negative values are likely errors and are removed to avoid misleading results.
    - **Remove rows with invoice numbers that start with 'C' (indicating cancellations):** Canceled transactions are not relevant for sales analysis and are removed.

4. **Feature Engineering:**
    - **Create a `TotalPrice` column representing the total price of each item:** This is calculated by multiplying the `UnitPrice` by the `Quantity`.

5. **Saving Cleaned Data:**
    - **Save the cleaned data to a CSV file:** The cleaned dataset is saved for future use and analysis.


### Data Analysis

After cleaning the data, various analytical tasks are performed to extract insights. The analysis includes identifying top 
countries and customers, calculating monthly revenue, and finding trends in product sales.

1. **Countries with High Returns:**
    - Identify the top 5 countries with the highest quantity of items sold and total price. This helps in understanding the 
geographic distribution of sales.

```python
# Countries with high returns
loyal_countries = df.groupby('Country').agg({
    'Quantity': 'sum',
    'TotalPrice': 'sum'
}).nlargest(5, 'Quantity')
```

2. **Most Loyal Customers:**
    - Identify the top 10 customers based on the quantity of items purchased and total price. This helps in recognizing the most valuable customers.

```python
# Most loyal customers
loyal_customer = df.groupby('CustomerID').agg({
    'Quantity': 'sum',
    'TotalPrice': 'sum'
}).nlargest(10, 'Quantity')
```

3. **Monthly Total Revenue:**
    - Calculate the total revenue generated each month. This helps in understanding the revenue trends over time.

```python
# Monthly total revenue
monthly_revenue = df.groupby('InvoiceMonth')['TotalPrice'].sum()
```

4. **Monthly Trend of Most Patronized Products:**
    - Determine the top 5 products based on quantity sold and analyze their monthly sales trend. This helps in identifying the most 
popular products and their sales trends.

```python
# Monthly trend of most patronized products (first five)
item_patronage = df.groupby('Description')['Quantity'].sum().nlargest(5)
item_patronage_df = df[df['Description'].isin(item_patronage.index)]
item_patronage_trend = item_patronage_df.groupby(['InvoiceMonth', 'Description'])['Quantity'].sum().unstack()
```

5. **Correlation Analysis:**
    - Plot the correlation between item quantities and unit price using a scatter plot. This helps in understanding the relationship 
between quantity and unit price.

```python
# Correlation between item quantities and unit price
import seaborn as sns

plt.scatter(df['Quantity'], df['UnitPrice'])
plt.title('Correlation Plot: Quantity vs UnitPrice')
plt.xlabel('Quantity')
plt.ylabel('Unit Price')
plt.grid(True)
plt.tight_layout()
plt.savefig('../../figures/EDA/scatter plot.jpg')
```

6. **Valuable Invoices and Items:**
    - Identify the top 5 invoices and top 10 items that yield the highest total returns. This helps in recognizing the most valuable 
transactions and products.

```python
# Invoice with the high returns (first five)
valuable_invoice = df.groupby('InvoiceNo')['TotalPrice'].sum().nlargest(5)

# Items that yield high returns (first ten)
valuable_items = df.groupby('Description')['TotalPrice'].sum().nlargest(10)
```

### Visualization

A scatter plot is generated to visualize the correlation between `Quantity` and `UnitPrice`. The plot is saved as an image file in 
the results directory. Visualizations help in better understanding the data and deriving actionable insights.

```python
# Correlation between item quantities and unit price
import seaborn as sns

plt.scatter(df['Quantity'], df['UnitPrice'])
plt.title('Correlation Plot: Quantity vs UnitPrice')
plt.xlabel('Quantity')
plt.ylabel('Unit Price')
plt.grid(True)
plt.tight_layout()
plt.savefig('../../figures/EDA/scatter plot.jpg')
```

## Conclusion

This script provides a comprehensive approach to cleaning, processing, and analyzing online retail sales data. The insights derived 
from the analysis can help in understanding customer behavior, product performance, and overall sales trends. The cleaned data and 
visualizations can be used for further analysis and decision-making.



---

By following this documentation, you can reproduce the analysis and extend it further based on your requirements. The structured approach 
ensures that the data is clean and reliable, and the analysis provides valuable insights into the online retail business.
