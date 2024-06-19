# online-retail-data-analysis
A comprehensive analysis on an online retail transaction data set for 13 months. The dataset is from [UCI Machine Learning Repository](https://www.kaggle.com/datasets/lakshmi25npathi/online-retail-dataset)<br><br>



This repository is a valuable resource for stakeholders interested in leveraging the power of data analytics to enhance business performance in the online retail sector. Through descriptive and advanced analytics, this project aims to uncover actionable insights to enhance understanding of customer behavior and inform strategic business decisions.
The insights here are designed to provide a comprehensive understanding of the various facets of customer behavior and business operations, to drive strategic business decisions and optimize operational efficiency as well as enhance customer satisfaction.
Key analyses into the intricate patterns of customer behavior and sales dynamics include:
- **Customer Clustering**: Identifying distinct customer segments using clustering algorithms so you can tailor marketing strategies and improve customer engagement.
- **Customer Lifetime Value (CLV)**: Calculating CLV to understand the long-term value of customers to gauge long-term profitability and prioritize high-value segments.
- **Customer Retention Analysis**: Analyzing retention rates and patterns to develop strategies to foster customer loyalty and reducing churn.
- **Daily Purchase Trends**: Investigating daily sales trends for operational insights, to aid in uncovering patterns and optimize inventory and sales strategies.
- **Customer Patronage Forecast**: Employing predictive models to forecast future customer purchases and demand, aiding in strategic planning.

Per the dataset, this analysis provides a general view of the customer journey and purchasing behaviors, equipping businesses with the insights needed to drive strategic decisions. By leveraging these insights, businesses can enhance operational efficiency, personalize customer experiences and ultimately boost profitability. 
That notwithstanding, the dataset does not have all the parameters to make a real-time decisions on business. Additional parameters (information) will be needed to make this analysis applicable in the real business setting – holistic. Also, the dataset is small; large dataset that spans multiple years is best suited for a complete analysis. Additional set of data worth considering are:
-	Marketing campaigns including paid advertisement (if any)
-	Customer feedback
-	Supply chain & Inventory data
-	Customer demographic data
-	Website analytics

# Note: 
I did an analysis on _items that are mostly purchased together_; I have the code for it, but it is **NOT TESTED!**.  My laptop memory (8GiB) cannot handle the (Apriori) algorithm that I used. I will be looking at rectifying this challenge. The result of this analysis has the potential to increase business gains.


# About Dataset
**InvoiceNo**: Invoice number. Nominal. A 6-digit integral number uniquely assigned to each transaction. If this code starts with the letter 'c', it indicates a cancellation.<br>
**StockCode**: Product (item) code. Nominal. A 5-digit integral number uniquely assigned to each distinct product.<br>
**Description**: Product (item) name. Nominal.<br>
**Quantity**: The quantities of each product (item) per transaction. Numeric.<br>
**InvoiceDate**: Invice date and time. Numeric. The day and time when a transaction was generated.<br>
**UnitPrice**: Unit price. Numeric. Product price per unit in sterling (Â£).<br>
**CustomerID**: Customer number. Nominal. A 5-digit integral number uniquely assigned to each customer.<br>
**Country**: Country name. Nominal. The name of the country where a customer resides.<br>
