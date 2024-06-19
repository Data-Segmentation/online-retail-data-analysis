'''
    This is part of the main program that deals with grouping customers
    based on their purchasing behavior. We can therefore classify new customers
    and predict their purchasing behavior
    Tools: K-means, Random Forest
'''

def customer_clusters(df):
    # aggregate customer data
    customer_data = df.groupby('CustomerID').agg({
        'Quantity': 'sum',
        'TotalPrice': 'sum',
        'InvoiceNo': 'nunique'
    }).rename(columns={'InvoiceNo': 'NumTransactions'}).reset_index()


    #   K-mean Clustering: create three groups (clusters)
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    # standardise data
    scaler = StandardScaler()
    customer_scaled = scaler.fit_transform(customer_data[['Quantity', 'TotalPrice', 'NumTransactions']])

    # apply clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    customer_data['Cluster'] = kmeans.fit_predict(customer_scaled)

    # profile clusters
    customer_data = customer_data.drop('CustomerID', axis=1)
    for cluster in range(3):
        cluster_data = customer_data[customer_data['Cluster'] == cluster]
        print(f'\nCluster {cluster} stats: \n', cluster_data.describe())


    # average characteristics of each cluster
    cluster_average = customer_data.groupby('Cluster').agg({
        'Quantity': 'mean',
        'NumTransactions': 'mean',
        'TotalPrice': 'mean'
    })

    # save data for customer classifications
    cluster_average.to_csv('output data/customer-clusters.csv')


    # determine the importance of each feature in a cluster
    from sklearn.ensemble import RandomForestClassifier

    # initialize Random Forest classifier, and fit model
    rf = RandomForestClassifier(random_state=42)
    x = customer_data[['Quantity', 'TotalPrice', 'NumTransactions']]
    y = customer_data['Cluster']
    rf.fit(x, y)

    # get feature importance scores
    feature_importance = rf.feature_importances_
    print('\nFeature Importance: ', feature_importance)

    # label clusters (according to your own metric)
    cluster_labels = {
        0: 'Low Frequency, Low Spend',
        1: 'High Frequency, High Spend',
        2: 'Medium Frequency, Medium Spend',
    }

    # map cluster numbers to labels
    customer_data['ClusterLabel'] = customer_data['Cluster'].map(cluster_labels)


    # predict cluster for new customers
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score

    # split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # initialize and train Random Forest classifier
    model = RandomForestClassifier(random_state=42)
    model.fit(x_train, y_train)

    # forecast for new set
    y_pred = model.predict(x_test)


    #   Evaluate Quality of Prediction
    # get model accuracy
    print(f'Prediction Accuracy: {accuracy_score(y_test, y_pred)}')

    from sklearn.metrics import silhouette_score, davies_bouldin_score

    # calculate silhouette score: how similar an object is to its own cluster
    # ranges from -1 t0 1: the higher, the better
    silhouette_avg = silhouette_score(customer_scaled, customer_data['Cluster'])
    print(f'Silhouette Score: {silhouette_avg}')

    # calculate Davies-Bouldin Index: how similar clusters are to each other
    # ranges from 0 to 1: the lower, the better
    db_index = davies_bouldin_score(customer_scaled, customer_data['Cluster'])
    print(f'Davies-Bouldin Index: {db_index}')

