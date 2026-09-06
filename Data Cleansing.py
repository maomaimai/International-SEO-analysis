import pandas as pd
import numpy as np
# Read the generated data
cleaned_df = pd.read_csv('cross_border_seo_data.csv')

# 1. Find the missing value
print("--- find the missing value ---")
print(cleaned_df.isnull().sum())

# 2. Clear the data according to the business logic: If conversions is zero, the revennue with NaN value should be zero

cleaned_df.loc[(cleaned_df['conversions'] == 0) & (cleaned_df['revenue_usd'].isnull()), 'revenue_usd'] = 0.0

# 3. If conversions > 0，but revenue is NaN，Using the median_aov * conversions replace the NaN
median_aov = 85.0
cleaned_df['revenue_usd'] = cleaned_df['revenue_usd'].fillna(cleaned_df['conversions'] * median_aov)

# 4. Make sure the data has been cleaned
print("--- Missing values after data cleaning ---")
print(cleaned_df.isnull().sum())

# 5. Output the final data for analysis of SQL and Tableau
cleaned_df.to_csv('seo_data_final.csv', index=False)
print("🚀 The final ready-to-analysis data document 'seo_data_final.csv' is ready！")
