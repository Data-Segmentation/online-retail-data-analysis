# Customer Lifetime Value (CLV) Analysis
This module is a part of a larger project focused on sales data analysis. It aims to calculate and analyze Customer Lifetime Value (CLV) 
using various machine learning techniques. This document provides an in-depth explanation of each section of the code, its relevance, 
and its implementation.

## Table of Contents

1. [Overview](#overview)
2. [Dependencies](#dependencies)
3. [Data Loading](#data-loading)
4. [RFM Analysis](#rfm-analysis)
5. [K-means Clustering](#k-means-clustering)
6. [Feature Engineering](#feature-engineering)
7. [Hyperparameter Tuning](#hyperparameter-tuning)
8. [Model Training and Evaluation](#model-training-and-evaluation)
9. [Feature Importance](#feature-importance)
10. [3D Cluster Plot](#3d-cluster-plot)
11. [Usage](#usage)
12. [License](#license)
<br>

## Overview

This module calculates the Customer Lifetime Value (CLV) by analyzing historical sales data. It uses the RFM (Recency, Frequency, Monetary) 
model to segment customers into clusters using K-means clustering. Further, it predicts the future value of customers using a Random Forest 
Regressor. The code also includes various evaluation metrics and visualizations to help understand the customer segments and their behavior.
<br>

## Dependencies

The code requires the following libraries:
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- mpl_toolkits

Ensure these packages are installed using pip (refer to [requirements]() for the specific versions):

```bash
pip install pandas numpy matplotlib seaborn scikit-learn mpl_toolkits
```
<br>

## Data Loading

### Function: `load_data`

```
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        return df
    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
        return None
```

This function loads the sales data from a CSV file and ensures that the `InvoiceDate` column is in datetime format. 
<br>

## RFM Analysis

### Function: `rfm_analysis`

```
def rfm_analysis(df):
    current_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (current_date - x.max()).days,
        'InvoiceNo': 'count',
        'TotalPrice': 'sum'
    }).reset_index()
    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
    return rfm
```

This function performs RFM analysis by calculating:
- **Recency:** Days since the last purchase.
- **Frequency:** Total number of purchases.
- **Monetary:** Total money spent.
<br>

## K-means Clustering

### Function: `perform_clustering`

```
def perform_clustering(rfm, n_clusters=5):
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])
    determine_optimal_clusters(rfm_scaled)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

    silhouette_avg = silhouette_score(rfm_scaled, rfm['Cluster'])
    davies_bouldin_avg = davies_bouldin_score(rfm_scaled, rfm['Cluster'])
    print(f'Silhouette Score: {silhouette_avg}')
    print(f'Davies-Bouldin Score: {davies_bouldin_avg}')
    
    return rfm, rfm_scaled
```

This function clusters customers based on their RFM values using K-means clustering. 
standardizes the RFM values, determines the optimal number of clusters using the Elbow method, 
and then applies K-means clustering to segment the customers. The resulting cluster labels are added to the RFM dataframe.
It also evaluates the clustering using silhouette and Davies-Bouldin scores.<br>
silhouette score measures how similar an object is to its own cluster: ranges from -1 to 1: the higher, the better <br>
Davies-Bouldin Index measures how similar clusters are to each other: ranges from 0 to 1: the lower, the better
<br>

## Feature Engineering

### Function: `feature_engineering`

```
def feature_engineering(df, rfm):
    df_clv = df.merge(rfm, on='CustomerID', how='left')
    features = df_clv.groupby('CustomerID').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean',
        'Cluster': 'mean',
        'Quantity': 'sum',
        'UnitPrice': 'mean'
    }).reset_index()
    features['histCLV'] = df_clv.groupby('CustomerID')['TotalPrice'].sum().values
    return features
```

This function prepares the data for modeling by creating relevant features that capture customer behavior.
It merges the original data with the RFM data, then calculates aggregated features like average recency, 
frequency, monetary value, and cluster label for each customer. It also computes the historical CLV.
<br>

## Hyperparameter Tuning

## Function: `hyperparameter_tuning`

```
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
```

Hyperparameter tuning optimizes the RandomForest model for better prediction accuracy by searching for the best set of hyperparameters.
It defines a parameter grid and uses `GridSearchCV` to find the best hyperparameters for the RandomForest model based on cross-validation performance.
<br>

## Model Training and Evaluation

### Function: `train_and_evaluate`

```
def train_and_evaluate(features):
    x = features[['Recency', 'Frequency', 'Monetary', 'Cluster', 'Quantity', 'UnitPrice']]
    y = features['histCLV']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
    
    model = hyperparameter_tuning(x_train, y_train)
    
    y_pred = model.predict(x_test)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    accuracy = accuracy_score(np.round(y_test / 100), np.round(y_pred / 100))
    print(f'MAPE: {mape}')
    print(f'Accuracy: {accuracy}')
    
    return model, x.columns
```

The function trains the RandomForest model on the engineered features and evaluates its performance using Mean Absolute Percentage Error (MAPE).
The data is split into training and testing sets. The best RandomForest model from hyperparameter tuning is used to predict CLV on the test set, 
and the performance is evaluated using MAPE.
<br>

## Feature Importance

### Function: `plot_feature_importance`

```
def plot_feature_importance(model, feature_names):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    plt.figure(figsize=(12, 6))
    plt.title('Feature Importances')
    plt.bar(range(len(importances)), importances[indices], align='center')
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices])
    plt.show()
```

This function plots the importance of each feature used in the model. Understanding feature importance 
helps in identifying which features are most influential in predicting CLV, providing insights for business strategies.
It extracts feature importances from the trained RandomForest model, sorts them, and plots them for visualization.
<br>

## 3D Cluster Plot

### Function: `plot_3d_clusters`

```
def plot_3d_clusters(rfm, rfm_scaled):
    minmax_scaler = MinMaxScaler()
    rfm_scaled_vis = minmax_scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(rfm_scaled_vis[:, 0], rfm_scaled_vis[:, 1], rfm_scaled_vis[:, 2], c=rfm['Cluster'], cmap='viridis')
    legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
    ax.add_artist(legend1)
    ax.set_xlabel('Recency')
    ax.set_ylabel('Frequency')
    ax.set_zlabel('Monetary')
    plt.show()
```

This function creates a 3D scatter plot of the clusters, allowing for visual interpretation of customer segments.
The plot uses `Recency`, `Frequency` and `Monetary` values on the x, y, and z axes respectively, and colors the points based on their cluster labels.
<br>

## Usage

To run the entire analysis, execute the `main()` function:

```
if __name__ == "__main__":
    main()
```

This will load the data, perform RFM analysis, cluster customers, engineer features, train the model and generate visualizations.



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

This detailed documentation covers various section of the code, explaining its purpose and implementation. It provides a clear understanding 
for anyone who wishes to use or contribute to the project.