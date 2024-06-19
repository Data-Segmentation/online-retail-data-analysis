'''
    This is part of the main program that deals with customer retention.
    Customers who made subsequent purchases after their first purchase;
    their percentage, quantity and returns
    Tools: Matplotlib, Seaborn
'''

def customer_retention(df):
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Convert InvoiceDate to datetime format
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Add a new column for the month and year of each invoice
    df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')

    # Create a dataframe to store the first purchase month of each customer
    customers = df.groupby('CustomerID').InvoiceMonth.min().reset_index()
    customers.columns = ['CustomerID', 'FirstPurchaseMonth']

    # Merge this information back into the original dataframe
    df = pd.merge(df, customers, on='CustomerID')

    # Create a cohort index based on the difference between InvoiceMonth and FirstPurchaseMonth
    df['CohortIndex'] = (df['InvoiceMonth'] - df['FirstPurchaseMonth']).apply(lambda x: x.n)

    # Count the number of unique customers and sum the monetary value in each cohort group
    cohort_data = df.groupby(['FirstPurchaseMonth', 'CohortIndex']).agg({
        'CustomerID': 'nunique',
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum'
    }).reset_index().rename(columns={'TotalPrice': 'MonetaryValue'})

    # Pivot the data for the number of customers and monetary value
    cohort_counts = cohort_data.pivot(index='FirstPurchaseMonth', columns='CohortIndex', values='CustomerID')
    cohort_monetary = cohort_data.pivot(index='FirstPurchaseMonth', columns='CohortIndex', values='MonetaryValue')

    # Calculate the retention rate
    cohort_size = cohort_counts.iloc[:, 0]
    retention = cohort_counts.divide(cohort_size, axis=0)

    # Plot the retention rate, number of customers, and monetary value
    fig, axes = plt.subplots(3, 1, sharex=True)

    # Plot retention rates
    sns.heatmap(retention, annot=True, fmt='.0%', cmap='coolwarm', ax=axes[0], annot_kws={'size': 6}, linewidths=1)
    axes[0].set_title('Monthly Customer Retention Rates')
    axes[0].set_xlabel('')
    axes[0].set_ylabel('First Purchase Month', fontsize=10)

    # Plot number of customers
    sns.heatmap(cohort_counts, annot=True, fmt='.0f', cmap='BuPu', ax=axes[1], annot_kws={'size': 6}, linewidths=1)
    axes[1].set_title('Number of Customers')
    axes[1].set_xlabel('')
    axes[1].set_ylabel('First Purchase Month', fontsize=10)

    # Plot monetary value
    sns.heatmap(cohort_monetary, annot=True, fmt='.2f', cmap='coolwarm', ax=axes[2], annot_kws={'size': 6}, linewidths=0.8)
    axes[2].set_title('Monetary Value')
    axes[2].set_xlabel('Cohort Index')
    axes[2].set_ylabel('First Purchase Month', fontsize=10)

    plt.savefig('output figures/customer-retention.jpg')
    plt.tight_layout()
    plt.show()


