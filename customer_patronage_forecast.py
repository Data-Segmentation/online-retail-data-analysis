'''
    This is part of the main program that deals with weekly patronage pattern.
    We make weekly predictions for the last 4 weeks of the dataset,
    and test the model's accuracy
    Tools: ARIMA, Matplotlib
'''

def customer_patronage_forecast(df):

    # weekly patronage prediction
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.stattools import adfuller
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    from sklearn.metrics import mean_absolute_percentage_error
    import matplotlib.pyplot as plt
    import pandas as pd

    # extract week from the date
    df['InvoiceWeek'] = df['InvoiceDate'].dt.isocalendar().week

    # group patronage by week
    patronage_weekly = df.groupby('InvoiceWeek')['CustomerID'].nunique().reset_index()
    patronage_weekly = patronage_weekly['CustomerID']

    # check stationarity
    result = adfuller(patronage_weekly, autolag='AIC')
    p_value = result[1]
    if p_value <= 0.05:
        d = 0
        data_diff = patronage_weekly
    else:
        d = 1  # Initial differencing step
        data_diff = patronage_weekly.diff().dropna()
        result_diff = adfuller(data_diff['InvoiceNo'])
        if result_diff[1] <= 0.05:
            pass
        else:
            # if series is still non-stationary, further differencing may be needed
            d = 2  # rare, typically d=1 is sufficient

    # identify model parameters
    plot_acf(data_diff)
    plt.savefig('output figures/cpf-acf-parameter-plot.jpg')
    plot_pacf(data_diff)
    plt.savefig('output figures/cpf-pacf-parameter-plot.jpg')
    plt.show()

    # define ARIMA parameters
    p, d, q = 1, 1, 1

    #   split data into training and testing sets
    train_data = patronage_weekly[:-4]
    test_data = patronage_weekly[-4:]   # data for last four weeks

    # fit the model
    model = ARIMA(train_data, order=(p, d, q))
    results = model.fit()

    # diagnostic plot
    results.plot_diagnostics()
    plt.savefig('output figures/cpf-diagnostic-plot.jpg')
    plt.show()

    # forecast for next quarter (12 weeks)
    forecast = results.get_forecast(steps=len(test_data))
    forecast_values = forecast.predicted_mean
    forecast_ci = forecast.conf_int()


    # Plot the original against the forecast
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.plot(patronage_weekly, color='navy')
    ax1.set_ylabel('Number of Customers', fontsize=10)
    ax1.set_xticks(range(1, 53))
    ax1.grid(True, linestyle='--')
    ax1.set_title('Weekly Customer Patronage', fontsize=10)

    ax2.plot(patronage_weekly, label='Original', color='olive')
    ax2.plot(train_data, label='Observed', color='navy')
    ax2.plot(forecast_values, label='Forecast (and range)', color='red')
    ax2.fill_between(forecast_ci.index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='pink')
    ax2.set_title('Weekly Customer Patronage Forecast Against Original', fontsize=10)
    ax2.set_xlabel('Week', fontsize=10)
    ax2.set_ylabel('Number of Customers', fontsize=10)
    ax2.set_xticklabels(range(1, 53), fontsize=8)
    ax2.grid(True, linestyle='--')
    ax2.legend()
    plt.tight_layout()
    plt.savefig('output figures/customer-patronage-forecast.jpg')
    plt.show()

    # check model accuracy
    mape = mean_absolute_percentage_error(test_data, forecast_values)
    print('mape: ', mape)

