# Customer Retention Analysis

This script performs a customer retention analysis by loading invoice data, processing it to determine cohorts, 
calculating retention rates, and visualizing the results in separate plots.
<br>

## Modules
- **pandas**: For data manipulation and analysis.
- **matplotlib.pyplot**: For creating static, animated, and interactive visualizations.
- **seaborn**: For making statistical graphics based on Matplotlib.
<br>

## Functions

### `load_data(filepath)`
Loads invoice data from a CSV file and parses the `InvoiceDate` column.

**Arguments:**
- `filepath` (str): Path to the CSV file.

**Returns:**
- `DataFrame`: Data with `InvoiceDate` parsed as datetime.

**Exceptions:**
- `FileNotFoundError`: If the file is not found.
- `pd.errors.EmptyDataError`: If the file is empty.
- `pd.errors.ParserError`: If there is a problem parsing the file.
- `Exception`: For any unexpected errors.

### `add_invoice_month(df)`
Adds a new column to the DataFrame indicating the month and year of each invoice.

**Arguments:**
- `df` (DataFrame): DataFrame containing invoice data.

**Returns:**
- `DataFrame`: Updated DataFrame with `InvoiceMonth` column.

**Exceptions:**
- `KeyError`: If the expected column is missing in the DataFrame.
- `Exception`: For any unexpected errors.

### `get_customer_first_purchase(df)`
Creates a DataFrame with the first purchase month for each customer.

**Arguments:**
- `df` (DataFrame): DataFrame containing invoice data.

**Returns:**
- `DataFrame`: DataFrame with `CustomerID` and their `FirstPurchaseMonth`.

**Exceptions:**
- `KeyError`: If the expected column is missing in the DataFrame.
- `Exception`: For any unexpected errors.

### `merge_customer_data(df, customers)`
Merges the first purchase month data back into the original DataFrame and calculates the cohort index.

**Arguments:**
- `df` (DataFrame): DataFrame containing invoice data.
- `customers` (DataFrame): DataFrame with `CustomerID` and their `FirstPurchaseMonth`.

**Returns:**
- `DataFrame`: Merged DataFrame with `FirstPurchaseMonth` and `CohortIndex` columns.

**Exceptions:**
- `KeyError`: If the expected column is missing in the DataFrame.
- `Exception`: For any unexpected errors.

### `compute_cohort_data(df)`
Computes cohort data including customer counts and monetary value.

**Arguments:**
- `df` (DataFrame): DataFrame containing invoice data with cohort information.

**Returns:**
- `tuple`: Two DataFrames containing cohort counts and cohort monetary values.

**Exceptions:**
- `KeyError`: If the expected column is missing in the DataFrame.
- `Exception`: For any unexpected errors.

### `calculate_retention_rate(cohort_counts)`
Calculates the retention rate from cohort counts as a percentage.

**Arguments:**
- `cohort_counts` (DataFrame): DataFrame with cohort counts.

**Returns:**
- `DataFrame`: Retention rates as a percentage.

**Exceptions:**
- `IndexError`: If the `cohort_counts` DataFrame is empty or incorrectly indexed.
- `Exception`: For any unexpected errors.

### `plot_cohort_analysis(retention, cohort_counts, cohort_monetary)`
Generates and saves separate plots for retention rates, number of customers, and monetary value.

**Arguments:**
- `retention` (DataFrame): DataFrame with retention rates.
- `cohort_counts` (DataFrame): DataFrame with cohort counts.
- `cohort_monetary` (DataFrame): DataFrame with cohort monetary values.

**Exceptions:**
- `FileNotFoundError`: If the directory for saving the plots does not exist.
- `Exception`: For any unexpected errors.

## Usage
1. Place your invoice data CSV file in the specified directory.
2. Set the `filepath` variable to the path of your CSV file.
3. Run the script. It will process the data, compute the necessary metrics, and generate plots saved in the `output_figures` directory.

## Dependencies

The code requires the following libraries:
- pandas
- numpy
- matplotlib
- seaborn

Ensure these packages are installed using pip (refer to [requirements]() for the specific versions):


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

