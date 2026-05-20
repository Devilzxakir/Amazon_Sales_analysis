"""
===============================================================
AMAZON E-COMMERCE SALES DATA CLEANING PROJECT
Enterprise-Grade Data Processing Pipeline
===============================================================
Author: Business Intelligence Analyst
Data Source: Amazon Sale Report.csv
Purpose: Clean, standardize, and prepare data for BI analysis
===============================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ================================================================
# CONFIGURATION
# ================================================================
INPUT_FILE = 'Amazon Sale Report.csv'
OUTPUT_DIR = 'cleaned_data/'
REPORT_DIR = 'reports/'

# ================================================================
# STEP 1: DATA LOADING
# ================================================================
print("=" * 70)
print("STEP 1: DATA LOADING")
print("=" * 70)

df = pd.read_csv(INPUT_FILE, low_memory=False)

print(f"Total Records Loaded: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")
print(f"\nOriginal Columns:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

# ================================================================
# STEP 2: INITIAL DATA EXPLORATION
# ================================================================
print("\n" + "=" * 70)
print("STEP 2: INITIAL DATA EXPLORATION")
print("=" * 70)

print("\n--- Data Types Summary ---")
print(df.dtypes)

print("\n--- First 5 Rows Sample ---")
print(df.head())

print("\n--- Basic Statistics ---")
print(df.describe())

# ================================================================
# STEP 3: MISSING VALUE ANALYSIS
# ================================================================
print("\n" + "=" * 70)
print("STEP 3: MISSING VALUE ANALYSIS")
print("=" * 70)

missing_report = pd.DataFrame({
    'Column': df.columns,
    'Missing Count': df.isnull().sum().values,
    'Missing Percentage': round((df.isnull().sum() / len(df) * 100), 2).values,
    'Data Type': df.dtypes.values
})
missing_report = missing_report.sort_values('Missing Percentage', ascending=False)
print("\n--- Missing Value Report ---")
print(missing_report.to_string(index=False))

# Save Missing Value Report
missing_report.to_csv(f'{REPORT_DIR}missing_value_report.csv', index=False)
print(f"\nMissing Value Report saved to: {REPORT_DIR}missing_value_report.csv")

# ================================================================
# STEP 4: DATA CLEANING OPERATIONS
# ================================================================
print("\n" + "=" * 70)
print("STEP 4: DATA CLEANING OPERATIONS")
print("=" * 70)

# 4.1: Create a copy for cleaning
df_clean = df.copy()
print("\n4.1: Created working copy of data")

# 4.2: Drop Unnamed columns
unnamed_cols = [col for col in df_clean.columns if 'Unnamed' in col]
if unnamed_cols:
    df_clean = df_clean.drop(columns=unnamed_cols)
    print(f"4.2: Dropped {len(unnamed_cols)} unnamed columns")

# 4.3: Drop index column if exists
if 'index' in df_clean.columns:
    df_clean = df_clean.drop(columns=['index'])
    print("4.3: Dropped 'index' column")

# 4.4: Date Formatting
print("\n4.4: Date Formatting...")
df_clean['Date'] = pd.to_datetime(df_clean['Date'], format='%m-%d-%y', errors='coerce')
print(f"  - Date column converted to datetime")
print(f"  - Date range: {df_clean['Date'].min()} to {df_clean['Date'].max()}")

# Extract Date Components
df_clean['Year'] = df_clean['Date'].dt.year
df_clean['Month'] = df_clean['Date'].dt.month
df_clean['Month_Name'] = df_clean['Date'].dt.month_name()
df_clean['Day'] = df_clean['Date'].dt.day
df_clean['Day_Name'] = df_clean['Date'].dt.day_name()
df_clean['Quarter'] = df_clean['Date'].dt.quarter
df_clean['Week'] = df_clean['Date'].dt.isocalendar().week
print("  - Extracted: Year, Month, Month_Name, Day, Day_Name, Quarter, Week")

# 4.5: Text Cleaning - Standardize City Names
print("\n4.5: Text Cleaning...")
df_clean['ship-city'] = df_clean['ship-city'].str.strip().str.upper()
df_clean['ship-state'] = df_clean['ship-state'].str.strip().str.upper()
print("  - City and State names standardized to UPPERCASE")

# 4.6: Clean Category Column
df_clean['Category'] = df_clean['Category'].str.strip().str.title()
print("  - Category names title-cased")

# 4.7: Clean Style Column
df_clean['Style'] = df_clean['Style'].str.strip().str.title()
print("  - Style names title-cased")

# 4.8: Clean Status Column
df_clean['Status'] = df_clean['Status'].str.strip()
print("  - Status column cleaned")

# 4.9: Handle Missing Amounts (Cancelled orders have 0 Amount)
print("\n4.9: Handling Missing Amounts...")
df_clean['Amount'] = pd.to_numeric(df_clean['Amount'], errors='coerce')
df_clean['Amount'] = df_clean['Amount'].fillna(0)
print(f"  - Missing Amounts filled with 0 (assuming Cancelled orders)")

# 4.10: Handle Missing Qty
df_clean['Qty'] = pd.to_numeric(df_clean['Qty'], errors='coerce')
df_clean['Qty'] = df_clean['Qty'].fillna(0)
print(f"  - Missing Qty filled with 0")

# 4.11: Clean Courier Status
df_clean['Courier Status'] = df_clean['Courier Status'].fillna('Unknown')
print("  - Courier Status missing values filled with 'Unknown'")

# 4.12: Clean Promotion IDs
df_clean['promotion-ids'] = df_clean['promotion-ids'].fillna('No Promotion')
print("  - Promotion IDs filled with 'No Promotion'")

# 4.13: Handle B2B Column
df_clean['B2B'] = df_clean['B2B'].astype(str).str.strip().str.lower() == 'true'
print("  - B2B column converted to boolean")

# 4.14: Clean Fulfilment Column
df_clean['Fulfilment'] = df_clean['Fulfilment'].str.strip()
print("  - Fulfilment column standardized")

# 4.15: Clean Sales Channel
df_clean['Sales Channel '] = df_clean['Sales Channel '].str.strip()
df_clean.rename(columns={'Sales Channel ': 'sales_channel'}, inplace=True)
print("  - Sales Channel renamed and standardized")

# 4.16: Clean ship-country
df_clean['ship-country'] = df_clean['ship-country'].str.strip().fillna('IN')
print("  - Ship country standardized")

# 4.17: Handle Postal Code
df_clean['ship-postal-code'] = df_clean['ship-postal-code'].fillna(0).astype(int)
print("  - Postal codes cleaned and converted to integer")

# ================================================================
# STEP 5: DUPLICATE REMOVAL
# ================================================================
print("\n" + "=" * 70)
print("STEP 5: DUPLICATE REMOVAL")
print("=" * 70)

# Check duplicates based on Order ID
duplicates_order = df_clean.duplicated(subset=['Order ID'], keep=False)
print(f"\nDuplicate Order IDs found: {duplicates_order.sum():,}")

# Keep only first occurrence of each Order ID
df_clean = df_clean.drop_duplicates(subset=['Order ID'], keep='first')
print(f"Duplicates removed. Records remaining: {len(df_clean):,}")

# Check full row duplicates
duplicates_full = df_clean.duplicated(keep=False)
print(f"Full row duplicates: {duplicates_full.sum()}")

# ================================================================
# STEP 6: OUTLIER DETECTION
# ================================================================
print("\n" + "=" * 70)
print("STEP 6: OUTLIER DETECTION")
print("=" * 70)

# 6.1: Amount Outliers using IQR method
Q1 = df_clean['Amount'].quantile(0.25)
Q3 = df_clean['Amount'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_amount = df_clean[(df_clean['Amount'] < lower_bound) | (df_clean['Amount'] > upper_bound)]
print(f"\n6.1: Amount Outliers (IQR Method):")
print(f"  - Q1: {Q1:.2f}, Q3: {Q3:.2f}, IQR: {IQR:.2f}")
print(f"  - Lower Bound: {lower_bound:.2f}, Upper Bound: {upper_bound:.2f}")
print(f"  - Outliers Found: {len(outliers_amount):,}")
print(f"  - Outlier Percentage: {len(outliers_amount)/len(df_clean)*100:.2f}%")

# 6.2: Quantity Outliers
Q1_qty = df_clean['Qty'].quantile(0.25)
Q3_qty = df_clean['Qty'].quantile(0.75)
IQR_qty = Q3_qty - Q1_qty
lower_bound_qty = Q1_qty - 1.5 * IQR_qty
upper_bound_qty = Q3_qty + 1.5 * IQR_qty

outliers_qty = df_clean[(df_clean['Qty'] < lower_bound_qty) | (df_clean['Qty'] > upper_bound_qty)]
print(f"\n6.2: Quantity Outliers:")
print(f"  - Outliers Found: {len(outliers_qty):,}")
print(f"  - Max Qty: {df_clean['Qty'].max()}, Min Qty: {df_clean['Qty'].min()}")

# 6.3: Z-Score Analysis for Amount
from scipy import stats
amounts = df_clean['Amount'].dropna()
z_scores = np.abs(stats.zscore(amounts))
outliers_zscore_count = int(np.sum(z_scores > 3))
print(f"\n6.3: Z-Score Analysis (threshold=3):")
print(f"  - Extreme outliers (Z>3): {outliers_zscore_count:,}")

# ================================================================
# STEP 7: COLUMN STANDARDIZATION (MUST HAPPEN BEFORE TYPE CONVERSION)
# ================================================================
print("\n" + "=" * 70)
print("STEP 7: COLUMN STANDARDIZATION")
print("=" * 70)

# Rename columns for consistency
column_mapping = {
    'Order ID': 'order_id',
    'Date': 'order_date',
    'Status': 'order_status',
    'Fulfilment': 'fulfilment_method',
    'Sales Channel ': 'sales_channel',
    'ship-service-level': 'ship_service_level',
    'Style': 'style',
    'SKU': 'sku',
    'Category': 'category',
    'Size': 'size',
    'ASIN': 'asin',
    'Courier Status': 'courier_status',
    'Qty': 'quantity',
    'currency': 'currency',
    'Amount': 'amount',
    'ship-city': 'city',
    'ship-state': 'state',
    'ship-postal-code': 'postal_code',
    'ship-country': 'country',
    'promotion-ids': 'promotion_ids',
    'B2B': 'b2b_flag',
    'fulfilled-by': 'fulfilled_by',
    'Year': 'year',
    'Month': 'month',
    'Month_Name': 'month_name',
    'Day': 'day',
    'Day_Name': 'day_name',
    'Quarter': 'quarter',
    'Week': 'week'
}

df_clean = df_clean.rename(columns=column_mapping)
print("Columns standardized:")
for old, new in column_mapping.items():
    print(f"  {old} -> {new}")

# ================================================================
# STEP 9: ADD DERIVED COLUMNS
# ================================================================
print("\n" + "=" * 70)
print("STEP 9: ADD DERIVED COLUMNS")
print("=" * 70)

# Revenue Classification
df_clean['revenue_tier'] = pd.cut(df_clean['amount'], 
                                   bins=[0, 500, 1000, 2000, float('inf')],
                                   labels=['Budget', 'Mid-Range', 'Premium', 'Luxury'])
print("9.1: Added revenue_tier classification")

# Order Size Classification
df_clean['order_size'] = pd.cut(df_clean['quantity'],
                                 bins=[0, 1, 2, 5, float('inf')],
                                 labels=['Single', 'Small', 'Medium', 'Large'])
print("9.2: Added order_size classification")

# Is Cancelled Flag
df_clean['is_cancelled'] = df_clean['order_status'].str.contains('Cancelled', case=False, na=False)
print("9.3: Added is_cancelled flag")

# Is Delivered Flag
df_clean['is_delivered'] = df_clean['order_status'].str.contains('Delivered', case=False, na=False)
print("9.4: Added is_delivered flag")

# Has Promotion Flag
df_clean['has_promotion'] = df_clean['promotion_ids'] != 'No Promotion'
print("9.5: Added has_promotion flag")

# Weekend Flag
df_clean['is_weekend'] = df_clean['day_name'].isin(['Saturday', 'Sunday'])
print("9.6: Added is_weekend flag")

# Season Classification
def get_season(month):
    if month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Autumn'
    else:
        return 'Winter'

df_clean['season'] = df_clean['month'].apply(get_season)
print("9.7: Added season classification")

# ================================================================
# STEP 10: FINAL DATA QUALITY REPORT
# ================================================================
print("\n" + "=" * 70)
print("STEP 10: FINAL DATA QUALITY REPORT")
print("=" * 70)

# Create comprehensive data quality report
quality_report = {
    'Metric': [
        'Total Records',
        'Total Columns',
        'Records After Cleaning',
        'Duplicates Removed',
        'Missing Values (Amount)',
        'Missing Values (Qty)',
        'Missing Values (Courier Status)',
        'Date Range Start',
        'Date Range End',
        'Unique Order IDs',
        'Unique Categories',
        'Unique States',
        'Unique Cities',
        'Total Revenue (INR)',
        'Average Order Value (INR)',
        'Cancellation Rate (%)',
        'Delivery Rate (%)',
        'B2B Orders (%)'
    ],
    'Value': [
        len(df),
        len(df.columns),
        len(df_clean),
        len(df) - len(df_clean),
        df_clean['amount'].isna().sum(),
        df_clean['quantity'].isna().sum(),
        df_clean['courier_status'].isna().sum(),
        str(df_clean['order_date'].min()),
        str(df_clean['order_date'].max()),
        df_clean['order_id'].nunique(),
        df_clean['category'].nunique(),
        df_clean['state'].nunique(),
        df_clean['city'].nunique(),
        round(df_clean['amount'].sum(), 2),
        round(df_clean['amount'].mean(), 2),
        round(df_clean['is_cancelled'].mean() * 100, 2),
        round(df_clean['is_delivered'].mean() * 100, 2),
        round(df_clean['b2b_flag'].mean() * 100, 2)
    ]
}

quality_df = pd.DataFrame(quality_report)
print("\n--- Data Quality Report ---")
print(quality_df.to_string(index=False))

# Save Data Quality Report
quality_df.to_csv(f'{REPORT_DIR}data_quality_report.csv', index=False)
print(f"\nData Quality Report saved to: {REPORT_DIR}data_quality_report.csv")

# ================================================================
# STEP 11: EXPORT CLEANED DATASET
# ================================================================
print("\n" + "=" * 70)
print("STEP 11: EXPORT CLEANED DATASET")
print("=" * 70)

# Export cleaned dataset
df_clean.to_csv(f'{OUTPUT_DIR}amazon_sales_cleaned.csv', index=False)
print(f"\nCleaned dataset exported to: {OUTPUT_DIR}amazon_sales_cleaned.csv")

# Export duplicate summary
duplicate_summary = pd.DataFrame({
    'Metric': ['Total Records (Before)', 'Total Records (After)', 'Duplicates Removed'],
    'Value': [len(df), len(df_clean), len(df) - len(df_clean)]
})
duplicate_summary.to_csv(f'{REPORT_DIR}duplicate_summary.csv', index=False)
print(f"Duplicate summary saved to: {REPORT_DIR}duplicate_summary.csv")

# ================================================================
# STEP 12: SUMMARY STATISTICS
# ================================================================
print("\n" + "=" * 70)
print("STEP 12: SUMMARY STATISTICS")
print("=" * 70)

print("\n--- Revenue Statistics ---")
print(f"Total Revenue: INR {df_clean['amount'].sum():,.2f}")
print(f"Average Order Value: INR {df_clean['amount'].mean():,.2f}")
print(f"Median Order Value: INR {df_clean['amount'].median():,.2f}")
print(f"Max Order Value: INR {df_clean['amount'].max():,.2f}")
print(f"Min Order Value: INR {df_clean['amount'].min():,.2f}")
print(f"Std Dev: INR {df_clean['amount'].std():,.2f}")

print("\n--- Order Status Distribution ---")
print(df_clean['order_status'].value_counts())

print("\n--- Category Distribution ---")
print(df_clean['category'].value_counts())

print("\n--- State Distribution ---")
print(df_clean['state'].value_counts().head(10))

print("\n--- Fulfilment Method Distribution ---")
print(df_clean['fulfilment_method'].value_counts())

print("\n--- Sales Channel Distribution ---")
print(df_clean['sales_channel'].value_counts())

print("\n--- Monthly Revenue Trend ---")
monthly = df_clean.groupby(['year', 'month', 'month_name'])['amount'].sum().reset_index()
monthly = monthly.sort_values(['year', 'month'])
print(monthly.to_string(index=False))

# ================================================================
# FINAL SUMMARY
# ================================================================
print("\n" + "=" * 70)
print("DATA CLEANING COMPLETE!")
print("=" * 70)
print(f"""
SUMMARY:
--------
- Input File: {INPUT_FILE}
- Original Records: {len(df):,}
- Cleaned Records: {len(df_clean):,}
- Records Removed: {len(df) - len(df_clean):,}
- Output File: {OUTPUT_DIR}amazon_sales_cleaned.csv
- Reports Generated: {REPORT_DIR}*

CLEANING OPERATIONS PERFORMED:
------------------------------
1. Removed {len(unnamed_cols)} unnamed columns
2. Converted dates to datetime format
3. Extracted date components (Year, Month, Quarter, etc.)
4. Standardized city and state names (UPPERCASE)
5. Cleaned category and style names
6. Handled missing Amount values (filled with 0)
7. Handled missing Qty values (filled with 0)
8. Converted B2B to boolean
9. Removed {len(df) - len(df_clean):,} duplicate Order IDs
10. Detected {len(outliers_amount):,} amount outliers
11. Standardized column names
12. Added derived columns (revenue_tier, order_size, etc.)
13. Data types optimized

NEXT STEPS:
-----------
1. Load cleaned CSV into MySQL database
2. Execute SQL business analysis queries
3. Create Power BI/Tableau dashboards
4. Generate business insights report
""")