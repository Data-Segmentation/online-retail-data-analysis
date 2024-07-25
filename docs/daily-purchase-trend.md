# Daily Purchase Trend Analysis

## Overview

This project aims to analyze daily purchase trends from sales data. The analysis involves loading the cleaned sales data, 
performing a time series decomposition to understand the seasonal and trend components, and visualizing the results. 
This helps in understanding purchasing patterns and identifying any significant trends or seasonal effects.

## Features

- **Data Loading:** Loads and validates sales data from a CSV file with robust error handling.
- **Data Validation:** Checks for required columns and validates data types to ensure the integrity of the data.
- **Data Processing:** Resamples the data to daily frequency and performs time series decomposition.
- **Visualization:** Generates and saves plots to visualize the sales trends and seasonal patterns.

## Getting Started

### Prerequisites

Ensure you have the following Python libraries installed:
- `pandas`
- `matplotlib`
- `statsmodels`

You can install these dependencies using pip:
```bash
pip install pandas matplotlib statsmodels
```

### File Structure

- `daily_purchase_trend.py`: The main script for data analysis and visualization.
- `../data/cleaned-data.csv`: The input CSV file containing cleaned sales data.
- `../results/figures/daily-trend/`: Directory where output figures will be saved.

### Script Description

The `daily_purchase_trend.py` script performs the following steps:

1. **Load Data**
   - Attempts to load the cleaned sales data from a specified CSV file.
   - Includes error handling for common issues such as file not found, empty file, or parsing errors.

2. **Data Validation**
   - Checks if the required columns (`InvoiceDate` and `TotalPrice`) are present in the DataFrame.
   - Validates that `InvoiceDate` is in datetime format and `TotalPrice` is numeric.

3. **Data Processing**
   - Sets the `InvoiceDate` column as the DataFrame index.
   - Resamples the data to daily frequency and computes the daily revenue.
   - Performs time series decomposition to extract trend, seasonal, and residual components.

4. **Visualization**
   - Plots and saves the decomposition of the sales trend.
   - Creates and saves a detailed plot showing the seasonal pattern for the first two weeks, with annotations for each day of the week.

### Error Handling

The script includes error handling for:
- File loading issues (e.g., file not found, empty file, parsing errors).
- Data validation issues (e.g., missing columns, incorrect data types).
- Processing issues during time series decomposition and plotting.

### Usage

To run the script, execute it from the command line:
```bash
python daily_purchase_trend.py
```

Ensure that the input file exists at the specified path (`../data/cleaned-data.csv`) and that the output directory 
(`../figures/daily-trend/`) exists or can be created.

### Example Output

- `purchase-trends.jpg`: A plot showing the decomposition of the sales trend into trend, seasonal, and residual components.
- `seasonal-plot.jpg`: A plot showing the purchase trend for the first two weeks with annotations indicating the day of the week.

## Contribution

Feel free to contribute to this project by submitting pull requests or opening issues. Contributions are welcome to improve the analysis, 
add new features, or fix bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This documentation provides a clear and detailed explanation of the project, its features, and how to use it. It should be helpful for anyone 
looking to understand or contribute to your project.
