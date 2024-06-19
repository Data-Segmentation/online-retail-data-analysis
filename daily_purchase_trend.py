'''
    This is part of the main program that deals with daily purchase trends and seasons;
    we also did create a seasonal plot of the first two weeks
    Tools: K-means, Random Forest
'''

def daily_purchase_trend(df):

    import pandas as pd
    import matplotlib.pyplot as plt
    from statsmodels.tsa.seasonal import seasonal_decompose

    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df.set_index('InvoiceDate', inplace=True)
    daily_revenue = df['TotalPrice'].resample('D').sum()
    purchase_trend = seasonal_decompose(daily_revenue, model='additive')
    purchase_trend.plot()
    plt.title('Sales Trend')
    plt.tight_layout()
    plt.savefig('figures/online-retail-store/purchase-trends.jpg')
    plt.show()

    #   sneak peek in to the seasonal plot
    seasonal = purchase_trend.seasonal
    seasonal_pattern = seasonal[:14]  # extract the first 14-days
    days_of_week = seasonal_pattern.index.strftime('%a')

    # identify each point with day
    for i, (date, value) in enumerate(seasonal_pattern.iteritems()):
        plt.annotate(days_of_week[i], (date, value), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.plot(seasonal_pattern, marker='o', ms=3)
    plt.xlabel('Day')
    plt.ylabel('purchase consistency')
    plt.title('Purchase Trend of First Two Weeks')
    plt.grid(axis='both')
    plt.tight_layout()
    plt.savefig('figures/online-retail-store/seasonal-plot.jpg')
    plt.show()