'''
    This module performs time series forecasting on customer patronage data using the ARIMA model.
    It includes functionalities for loading and preprocessing data, checking stationarity,
    fitting an ARIMA model, predicting patronage, and evaluating model performance.
'''


import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_absolute_percentage_error

# Load data with error handling
try:
    df = pd.read_csv('../data/processed/cleaned-data.csv')
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
    # Extract week from the date
    try:
        df['InvoiceWeek'] = df['InvoiceDate'].dt.isocalendar().week
    except Exception as e:
        print(f"Error while extracting weeks from dates: {e}")
        df = None

    if df is not None:
        # Group patronage by week
        try:
            patronage_weekly = df.groupby('InvoiceWeek')['CustomerID'].nunique().reset_index()
            patronage_weekly = patronage_weekly['CustomerID']
        except Exception as e:
            print(f"Error while grouping patronage by week: {e}")
            df = None

        if df is not None:
            # Check stationarity
            try:
                result = adfuller(patronage_weekly, autolag='AIC')
                p_value = result[1]
                if p_value <= 0.05:
                    d = 0
                    data_diff = patronage_weekly
                else:
                    d = 1  # Initial differencing step
                    data_diff = patronage_weekly.diff().dropna()
                    result_diff = adfuller(data_diff)
                    if result_diff[1] <= 0.05:
                        pass
                    else:
                        # if series is still non-stationary, further differencing may be needed
                        d = 2  # rare, typically d=1 is sufficient
            except Exception as e:
                print(f"Error during stationarity check: {e}")
                df = None

            if df is not None:
                # Identify model parameters
                try:
                    plot_acf(data_diff)
                    plt.savefig('../figures/customer-patronage-forecast/cpf-acf-parameter-plot.jpg')
                    plot_pacf(data_diff)
                    plt.savefig('../figures/customer-patronage-forecast/cpf-pacf-parameter-plot.jpg')
                except Exception as e:
                    print(f"Error while plotting ACF and PACF: {e}")

                # Define ARIMA parameters
                p, d, q = 1, 1, 1

                # Split data into training and testing sets
                try:
                    train_data = patronage_weekly[:-4]
                    test_data = patronage_weekly[-4:]   # data for last four weeks
                except Exception as e:
                    print(f"Error while splitting data into training and testing sets: {e}")

                if df is not None:
                    # Fit the model
                    try:
                        model = ARIMA(train_data, order=(p, d, q))
                        results = model.fit()
                    except Exception as e:
                        print(f"Error while fitting ARIMA model: {e}")

                    if df is not None:
                        # Diagnostic plot
                        try:
                            results.plot_diagnostics()
                            plt.savefig('../figures/customer-patronage-forecast/cpf-diagnostic-plot.jpg')
                        except Exception as e:
                            print(f"Error while plotting diagnostics: {e}")

                        # Forecast for next quarter (12 weeks)
                        try:
                            forecast = results.get_forecast(steps=len(test_data))
                            forecast_values = forecast.predicted_mean
                            forecast_ci = forecast.conf_int()
                        except Exception as e:
                            print(f"Error while forecasting: {e}")

                        if df is not None:
                            # Plot the original against the forecast
                            try:
                                fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
                                ax1.plot(patronage_weekly, color='navy')
                                ax1.set_ylabel('Number of Customers', fontsize=10)
                                ax1.set_xticks(range(1, 53))
                                ax1.grid(True, linestyle='--')
                                ax1.set_title('Weekly Customer Patronage', fontsize=10)

                                ax2.plot(patronage_weekly, label='Original', color='olive')
                                ax2.plot(train_data, label='Observed', color='navy')
                                ax2.plot(forecast_values, label='Forecast (with range)', color='red')
                                ax2.fill_between(forecast_ci.index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='pink')
                                ax2.set_title('Weekly Customer Patronage Forecast Against Original', fontsize=10)
                                ax2.set_xlabel('Week', fontsize=10)
                                ax2.set_ylabel('Number of Customers', fontsize=10)
                                ax2.set_xticklabels(range(1, 53), fontsize=8)
                                ax2.grid(True, linestyle='--')
                                ax2.legend()
                                plt.tight_layout()
                                plt.savefig('../figures/customer-patronage-forecast/customer-patronage-forecast.jpg')
                            except Exception as e:
                                print(f"Error while plotting forecast: {e}")

                            # Check model accuracy
                            try:
                                mape = mean_absolute_percentage_error(test_data, forecast_values)
                                print('MAPE:', mape)
                            except Exception as e:
                                print(f"Error while calculating MAPE: {e}")
