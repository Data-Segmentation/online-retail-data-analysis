'''
    This is part of the main program that deals with customer life value;
    determine the returns of customers, and determine future trend
    Tools: K-means, Random Forest
'''

def customer_life_value(df):
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    #   RFM Analysis
    current_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (current_date - x.max()).days,
        'InvoiceNo': 'count',
        'TotalPrice': 'sum'
    }).reset_index()
    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

    #   K-means Clustering: only done on columns with numerical entries
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

    kmeans = KMeans(n_clusters=5, random_state=42)
    rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

    #   make predictions for CLV
    # merge rfm data with original data
    df_clv = df.merge(rfm, on='CustomerID', how='left')

    features = df_clv.groupby('CustomerID').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean',
        'Cluster': 'mean',
        'Quantity': 'sum',
        'UnitPrice': 'mean'
    }).reset_index()

    # get historical CLV values
    features['histCLV'] = df_clv.groupby('CustomerID')['TotalPrice'].sum().values

    # train model
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_percentage_error

    x = features[['Recency', 'Frequency', 'Monetary', 'Cluster', 'Quantity', 'UnitPrice']]
    y = features['histCLV']

    # split and train model
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    # predict and evaluate model
    y_pred = model.predict(x_test)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    print(f'MAPE: {mape}')

    #   average characteristics of each cluster
    cluster_summary = rfm.groupby('Cluster').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean',
        'CustomerID': 'count'
    }).reset_index()

