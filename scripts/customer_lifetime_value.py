'''
    This script provides a comprehensive approach to customer lifetime value analysis by integrating RFM analysis,
    clustering, feature engineering, model training and evaluation. It also incorporates hyperparameter tuning and
    feature importance analysis
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error, silhouette_score, davies_bouldin_score, accuarcy_score
from sklearn.model_selection import train_test_split, GridSearchCV

# load data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        return df
    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
        return None

# RFM Analysis
def rfm_analysis(df):
    current_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (current_date - x.max()).days,
        'InvoiceNo': 'count',
        'TotalPrice': 'sum'
    }).reset_index()
    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
    return rfm

# Determine optimal number of clusters using the Elbow method
def determine_optimal_clusters(rfm_scaled):
    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(rfm_scaled)
        sse.append(kmeans.inertia_)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), sse, marker='o')
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('SSE')
    plt.savefig('../figures/CLV/elbow-plot.jpg')

# K-means Clustering
def perform_clustering(rfm, n_clusters=5):
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])
    determine_optimal_clusters(rfm_scaled)  # Show the Elbow method plot

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

    # evaluate clustering
    silhouette_avg = silhouette_score(rfm_scaled, rfm['Cluster'])
    davies_bouldin_avg = davies_bouldin_score(rfm_scaled, rfm['Cluster'])
    print(f'Silhouette Score: {silhouette_avg}')
    print(f'Davies-Bouldin Score: {davies_bouldin_avg}')

    # label clusters
    rfm['Cluster'] = rfm['Cluster'].map({
        0: 'Cluster 1',
        1: 'Cluster 2',
        2: 'Cluster 3',
        3: 'Cluster 4',
        4: 'Cluster 5'
    })

    return rfm, rfm_scaled

# Feature Engineering
def feature_engineering(df, rfm):
    # Merge RFM data with original data
    df_clv = df.merge(rfm, on='CustomerID', how='left')

    # Convert non-numeric columns to numeric where appropriate
    df_clv['Quantity'] = pd.to_numeric(df_clv['Quantity'], errors='coerce')
    df_clv['UnitPrice'] = pd.to_numeric(df_clv['UnitPrice'], errors='coerce')

    # Convert 'Cluster' to numeric codes
    df_clv['Cluster'] = df_clv['Cluster'].astype('category').cat.codes

    # Handle missing values
    df_clv.fillna({
        'Quantity': df_clv['Quantity'].mean(),
        'UnitPrice': df_clv['UnitPrice'].mean()
    }, inplace=True)

    # Aggregate features
    features = df_clv.groupby('CustomerID').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean',
        'Cluster': 'mean',
        'Quantity': 'sum',
        'UnitPrice': 'mean'
    }).reset_index()

    # Ensure 'histCLV' is numeric
    features['histCLV'] = df_clv.groupby('CustomerID')['TotalPrice'].sum().values

    return features


# Hyperparameter Tuning for RandomForest
def hyperparameter_tuning(x_train, y_train):
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    rf = RandomForestRegressor(random_state=42)
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(x_train, y_train)
    return grid_search.best_estimator_

# Model Training and Evaluation
def train_and_evaluate(features):
    x = features[['Recency', 'Frequency', 'Monetary', 'Cluster', 'Quantity', 'UnitPrice']]
    y = features['histCLV']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    model = hyperparameter_tuning(x_train, y_train)  # Get the best model after hyperparameter tuning

    y_pred = model.predict(x_test)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    accuracy = np.mean(np.round(y_test / 100) == np.round(y_pred / 100))
    print(f'MAPE: {mape}')
    print(f'Accuracy: {accuracy}')

    return model, x.columns

# Feature Importance Analysis
def plot_feature_importance(model, feature_names):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    plt.figure(figsize=(12, 6))
    plt.title('Feature Importances')
    plt.bar(range(len(importances)), importances[indices], align='center')
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices])
    plt.savefig('../figures/CLV/feature-importance.jpg')

# 3D Plot of Clusters
def plot_3d_clusters_with_labels(rfm):
    # Convert cluster labels to numeric codes
    rfm['Cluster_Code'] = rfm['Cluster'].astype('category').cat.codes

    # Use MinMaxScaler for visualization to avoid negative values
    minmax_scaler = MinMaxScaler()
    rfm_scaled_vis = minmax_scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot with numeric cluster codes
    scatter = ax.scatter(rfm_scaled_vis[:, 0], rfm_scaled_vis[:, 1], rfm_scaled_vis[:, 2],
                         c=rfm['Cluster_Code'], cmap='viridis', s=50, alpha=0.7)

    # Add legend with cluster labels
    labels = {i: f'Cluster {i + 1}' for i in range(rfm['Cluster_Code'].nunique())}
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=scatter.cmap(scatter.norm(i)), markersize=10)
               for i in labels.keys()]
    legend1 = ax.legend(handles, labels.values(), title="Clusters")
    ax.add_artist(legend1)

    ax.set_xlabel('Recency')
    ax.set_ylabel('Frequency')
    ax.set_zlabel('Monetary')
    ax.set_title('3D Plot of Customer Clusters')

    plt.savefig('../figures/CLV/clusters.jpg')


def profile_clusters(rfm):
    cluster_profiles = {}
    for cluster in rfm['Cluster'].unique():
        cluster_profiles[cluster] = rfm[rfm['Cluster'] == cluster].describe()
        print(f'Cluster {cluster} Profile:\n{cluster_profiles[cluster]}\n')
    return cluster_profiles

# Main function to run the analyses
def main():
    filepath = '../data/cleaned-data.csv'
    df = load_data(filepath)
    if df is not None:
        rfm = rfm_analysis(df)
        rfm, rfm_scaled = perform_clustering(rfm, n_clusters=5)
        features = feature_engineering(df, rfm)
        model, feature_names = train_and_evaluate(features)
        plot_feature_importance(model, feature_names)
        plot_3d_clusters_with_labels(rfm)
        profile_clusters(rfm)

        # Cluster Summary
        cluster_summary = rfm.groupby('Cluster').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean',
            'CustomerID': 'count'
        }).reset_index()
        print('Cluster Summary:\n', cluster_summary)


if __name__ == "__main__":
    main()
