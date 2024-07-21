# Online Sales Data Analyses

## Overview
A comprehensive analysis on an online retail transaction data set for 13 months. The dataset is from 
[UCI Machine Learning Repository](https://www.kaggle.com/datasets/lakshmi25npathi/online-retail-dataset)<br>

This repository is a valuable resource for stakeholders interested in leveraging the power of data analytics 
to enhance business performance in the online retail sector. Through descriptive and advanced analytics, this 
project aims to uncover actionable insights to enhance understanding of customer behavior and inform strategic 
business decisions.

## About Dataset
**InvoiceNo**: Invoice number. Nominal. A 6-digit integral number uniquely assigned to each transaction. If this 
code starts with the letter 'c', it indicates a cancellation.<br>
**StockCode**: Product (item) code. Nominal. A 5-digit integral number uniquely assigned to each distinct product.<br>
**Description**: Product (item) name. Nominal.<br>
**Quantity**: The quantities of each product (item) per transaction. Numeric.<br>
**InvoiceDate**: Invice date and time. Numeric. The day and time when a transaction was generated.<br>
**UnitPrice**: Unit price. Numeric. Product price per unit in sterling (Â£).<br>
**CustomerID**: Customer number. Nominal. A 5-digit integral number uniquely assigned to each customer.<br>
**Country**: Country name. Nominal. The name of the country where a customer resides.<br>


## Project Structure
The project is organized into the following directories:


Online_Sales_Data_Analysis/<br>
<img src="https://github.com/Data-Segmentation/online-retail-data-analysis/blob/main/images/project-structure.JPG">


### Description of Directories
- **data/**: This directory contains all data-related files.
  - `raw/`: Contains raw data files as received from the source.
  - `processed/`: Contains data that has been cleaned and processed.

- **docs/**: Documentations for different stages of the project.
  - `customer-lifetime-value.md`: calculation and analysis of CLV.
  - `customer-retention.md`: Data processing to determine cohorts and retention rates.
  - `daily-purchase-trend.md`: Analysis of sales data including trends, patterns, and key metrics.
  - `customer-patronage-forecast.md`: Analysis of customer behavior over time.
  - `data-processing.md`: Initial processing to clean data and derive insights.

- **scripts/**: Python scripts for automated data processing and analysis.
  - `EDA/`: contains scripts for data cleaning and preprocessing, as well as descriptive analysis.
  - `customer_lifetime_value.py`: Script for determining Customer Lifetime Value.
  - `customer_patronage_forecast.py`: Script for predicting customer behavior.
  - `customer_retention.py`: Script for calculating customer retention rates.
  - `daily_purchase_trend.py`: Script for determining purchase trends.

- **figures/**: Generated plots/visualizations for the respective scritps.


## Installation
Clone the repository and install the necessary dependencies using `pip`:
```bash
git clone https://github.com/your-username/online-sales-data-analysis.git
cd online-retail-data-analysis
pip install -r requirements.txt
```

## Usage
1. **EDA**: Run the scripts in this directory to clean and preprocess; understand the dataset.
    ```bash
    python scripts/EDA/*.py
    ```

2. **Customer Lifetime Value**: Calculate the CLV.
    ```bash
    python scripts/customer_lifetime_value.py
    ```

3. **Customer Patronage Forecast**: Determine customer behavior and make predictions.
    ```bash
    python scripts/customer_patronage_forecast.py
    ```

4. **Customer Retention**: Determine customer retention rates.
    ```bash
    python scripts/customer_retention.py
    ```

## Project Modules
### Exploatory Data Analysis
This is a directory containing modules for data preprocessing:
- Cleaning the data by handling missing values, duplicates, cancelled entries amongst others
- Initial understanding of the dataset.
- Identifying key variables and their distributions
- Transforming data types and normalizing values as needed.
- Feature engineering to create new relevant features.

### Customer Lifetime Value
The analysis module covers:
- Recency, Frequency and Monetary (RFM) Anlysis of customers.
- Segmenting customers based on their purchasing behavior, based on RFM.
- Feature engineering and hyperparameter tuning to find best dataset for building model.
- Evaluation of model, and features' contributions in the developed model
- Visualisation of segments (clusters) in a 3D plot

### Customer Retention
The customer retention module focuses on:
- Creating first purchase month for each customer
- Assigning cohorts to customers based on their first purchase month - cohort index
- Computing for each cohort, the number of customers, the monetery value and rentention rates

### Customer Patronage Forecast
The customer patronage forecast module focuses on:
- Grouping the dataset to have weekly entries
- Determining the appropriate parameters to fit model
- Making weekly predictions for customer patronage behavior

### Daily Purchase Trend
The daily purchase trend module focuses on:
- Resampling dataset to have daily entries and revenue
- Checking for trends and seasonalities in the dataset
- Creating visualisation of purchase pattern for the first few weeks

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests with any improvements or additional features.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details..

## Note: 
I did an analysis on _items that are mostly purchased together_; I have the code for it, but it is **NOT TESTED!**.  
My laptop memory (8GiB) cannot handle the (Apriori) algorithm that I used. I will be looking at rectifying this 
challenge. The result of this analysis has the potential to increase business gains.

---

This README.md file provides a clear and organized structure for "Online Sales Data Analysis" project. It includes sections for project 
overview, installation instructions, usage guidelines, and references to each project module.
