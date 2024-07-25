'''
    This script performs an analysis of daily purchase trends. It begins by loading and validating
    the data, checking for necessary columns and correct data types. The script then processes the
    data by resampling it to a daily frequency and conducting a time series decomposition to extract
    and visualize trend, seasonal, and residual components.
'''

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Load data with error handling
try:
    df = pd.read_csv('../data/cleaned-data.csv')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
except FileNotFoundError:
    print("Error: The file was not found. Please check the file path.")
    df = None
except pd.errors.EmptyDataError:
    print("Error: The file is empty. Please provide a valid data file.")
    df = None
except pd.errors.ParserError:
    print("Error: The file could not be parsed. Please check the file format.")
    df = None

if df is not None:
    # Check for required columns
    required_columns = ['InvoiceDate', 'TotalPrice']
    if not all(col in df.columns for col in required_columns):
        print(f"Error: The DataFrame is missing one or more required columns: {required_columns}")
        df = None
    else:
        # Validate data types
        if not pd.api.types.is_datetime64_any_dtype(df['InvoiceDate']):
            print("Error: 'InvoiceDate' column is not in datetime format.")
            df = None
        elif not pd.api.types.is_numeric_dtype(df['TotalPrice']):
            print("Error: 'TotalPrice' column is not numeric.")
            df = None

if df is not None:
    # Proceed with data processing
    try:
        df.set_index('InvoiceDate', inplace=True)

        # Resample the data to get daily revenue
        daily_revenue = df['TotalPrice'].resample('D').sum()

        # Decompose the time series
        purchase_trend = seasonal_decompose(daily_revenue, model='additive')

        # Plot the decomposition
        plt.figure(figsize=(12, 8))
        purchase_trend.plot()
        plt.suptitle('Sales Trend Decomposition', fontsize=16)
        plt.tight_layout()
        plt.savefig('../figures/daily-trend/purchase-trends.jpg')

        # Sneak peek into the seasonal plot
        seasonal = purchase_trend.seasonal
        seasonal_pattern = seasonal[:14]  # Extract the first 14-days

        # Improve the day labels
        days_of_week = seasonal_pattern.index.strftime('%a')

        # Create a plot for the first two weeks
        plt.figure(figsize=(10, 6))
        plt.plot(seasonal_pattern, marker='o', linestyle='-', color='b', markersize=6)
        plt.xlabel('Day', fontsize=12)
        plt.ylabel('Purchase Consistency', fontsize=12)
        plt.title('Purchase Trend of the First Two Weeks', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Annotate each point with the day of the week
        for i, (date, value) in enumerate(seasonal_pattern.items()):
            plt.annotate(days_of_week[i], (date, value), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, color='red')

        plt.tight_layout()
        plt.savefig('../figures/daily-trend/seasonal-plot.jpg')

    except KeyError as e:
        print(f"Error: KeyError encountered during processing. {e}")
    except ValueError as e:
        print(f"Error: ValueError encountered during processing. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

else:
    print("DataFrame is not loaded. Please check the errors above and try again.")
