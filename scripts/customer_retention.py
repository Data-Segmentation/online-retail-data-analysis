"""
    This script performs a customer retention analysis by processing invoice data
    to calculate and visualize retention rates, cohort sizes, and monetary values.
    It generates separate heatmaps to display retention rates, customer
    counts, and monetary values
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        return df
    except FileNotFoundError:
        print("Error: The file was not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

# add new column for month & year
def add_invoice_month(df):
    try:
        df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')
        return df
    except KeyError as e:
        print(f"Error: Missing expected column in DataFrame: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return df

# determine first purchase month for each customer
def get_customer_first_purchase(df):
    try:
        customers = df.groupby('CustomerID').InvoiceMonth.min().reset_index()
        customers.columns = ['CustomerID', 'FirstPurchaseMonth']
        return customers
    except KeyError as e:
        print(f"Error: Missing expected column in DataFrame: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return pd.DataFrame()

# merge first purchase month to original dataframe
def merge_customer_data(df, customers):
    try:
        df = pd.merge(df, customers, on='CustomerID')
        df['CohortIndex'] = (df['InvoiceMonth'] - df['FirstPurchaseMonth']).apply(lambda x: x.n)
        return df
    except KeyError as e:
        print(f"Error: Missing expected column in DataFrame: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return df

# compute cohort data: customer counts and monetary values
def compute_cohort_data(df):
    try:
        cohort_data = df.groupby(['FirstPurchaseMonth', 'CohortIndex']).agg({
            'CustomerID': 'nunique',
            'InvoiceNo': 'nunique',
            'TotalPrice': 'sum'
        }).reset_index().rename(columns={'TotalPrice': 'MonetaryValue'})

        cohort_counts = cohort_data.pivot(index='FirstPurchaseMonth', columns='CohortIndex', values='CustomerID')
        cohort_monetary = cohort_data.pivot(index='FirstPurchaseMonth', columns='CohortIndex', values='MonetaryValue')

        return cohort_counts, cohort_monetary
    except KeyError as e:
        print(f"Error: Missing expected column in DataFrame: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return pd.DataFrame(), pd.DataFrame()

# calculate retention rate
def calculate_retention_rate(cohort_counts):
    try:
        cohort_size = cohort_counts.iloc[:, 0]
        retention = cohort_counts.divide(cohort_size, axis=0)
        return retention
    except IndexError:
        print("Error: Cohort counts DataFrame is empty or incorrectly indexed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return pd.DataFrame()

# visualise data
def plot_cohort_analysis(retention, cohort_counts, cohort_monetary):
    try:
        # Plot retention rates
        plt.figure(figsize=(10, 6))
        sns.heatmap(retention, annot=True, fmt='.0%', cmap='coolwarm', linewidths=1)
        plt.title('Monthly Customer Retention Rates')
        plt.xlabel('Cohort Index')
        plt.ylabel('First Purchase Month')
        plt.savefig('../figures/customer-retention/retention-rates.jpg')
        plt.close()

        # Plot number of customers
        plt.figure(figsize=(10, 6))
        sns.heatmap(cohort_counts, annot=True, fmt='.0f', cmap='BuPu', linewidths=1)
        plt.title('Number of Customers')
        plt.xlabel('Cohort Index')
        plt.ylabel('First Purchase Month')
        plt.savefig('../figures/customer-retention/number-of-customers.jpg')
        plt.close()

        # Plot monetary value
        plt.figure(figsize=(14, 10))
        sns.heatmap(cohort_monetary, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.8, annot_kws={'size': 8})
        plt.title('Monetary Value', fontsize=14)
        plt.xlabel('Cohort Index', fontsize=12)
        plt.ylabel('First Purchase Month', fontsize=12)
        plt.tight_layout()
        plt.savefig('../figures/customer-retention/monetary-value.jpg')
        plt.close()

    except FileNotFoundError:
        print("Error: Directory for saving the plots does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Main script execution
if __name__ == "__main__":
    filepath = '../data/processed/cleaned-data.csv'
    df = load_data(filepath)

    if df is not None:
        df = add_invoice_month(df)
        customers = get_customer_first_purchase(df)
        if not customers.empty:
            df = merge_customer_data(df, customers)
            cohort_counts, cohort_monetary = compute_cohort_data(df)
            if not cohort_counts.empty:
                retention = calculate_retention_rate(cohort_counts)
                plot_cohort_analysis(retention, cohort_counts, cohort_monetary)
