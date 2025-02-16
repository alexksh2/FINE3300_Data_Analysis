import pandas as pd
from dateutil import parser

# QUESTION 1

# Import data from each csv file into a dataframe
province_ab = pd.read_csv("A2 Data/AB.CPI.1810000401.csv")
province_bc = pd.read_csv("A2 Data/BC.CPI.1810000401.csv")
province_mb = pd.read_csv("A2 Data/MB.CPI.1810000401.csv")
province_nb = pd.read_csv("A2 Data/NB.CPI.1810000401.csv")
province_nl = pd.read_csv("A2 Data/NL.CPI.1810000401.csv")
province_ns = pd.read_csv("A2 Data/NS.CPI.1810000401.csv")
province_on = pd.read_csv("A2 Data/ON.CPI.1810000401.csv")
province_pei = pd.read_csv("A2 Data/PEI.CPI.1810000401.csv")
province_qc = pd.read_csv("A2 Data/QC.CPI.1810000401.csv")
province_sk = pd.read_csv("A2 Data/SK.CPI.1810000401.csv")
overall_canada = pd.read_csv("A2 Data/Canada.CPI.1810000401.csv")

# Function to detect and standardize date format
def standardize_month_format(month_str):
    try:
        # Parse the date automatically
        date_obj = parser.parse(month_str, fuzzy=True)
        return date_obj.strftime("%b-%d")  # Convert to 'MMM DD' format
    except Exception:
        print('warning')
        return month_str  # Return original if parsing fails

def transform_df(df,name):
    df = df.iloc[:,:13]
    df.columns = ["Item"] + [standardize_month_format(month) for month in df.columns[1:]]
    df_transformed = df.melt(id_vars=["Item"], var_name="Month", value_name="CPI")
    df_transformed["Jurisdiction"] = name
    return df_transformed

# Transform the dataframes into appropriate format
province_ab_transformed = transform_df(province_ab,"Alberta")
province_bc_transformed = transform_df(province_bc,"British Columbia")
province_mb_transformed = transform_df(province_mb,"Manitoba")
province_nb_transformed = transform_df(province_nb,"New Brunswick")
province_nl_transformed = transform_df(province_nl,"Newfoundland and Labrador")
province_ns_transformed = transform_df(province_ns,"Nova Scotia")
province_on_transformed = transform_df(province_on,"Ontario")
province_pei_transformed = transform_df(province_pei,"Prince Edward Island")
province_qc_transformed = transform_df(province_qc,"Quebec")
province_sk_transformed = transform_df(province_sk,"Saskatchewan")

overall_canada_transformed = transform_df(overall_canada,"Canada")

# Concatenate the dataframes
all_provinces = [overall_canada_transformed,province_ab_transformed,province_bc_transformed,
                 province_mb_transformed,province_nb_transformed,province_nl_transformed,province_ns_transformed,
                 province_on_transformed,province_pei_transformed,province_qc_transformed,province_sk_transformed]
combined_df = pd.concat(all_provinces)
# Rearrange the columns
combined_df = combined_df[["Item","Month","Jurisdiction","CPI"]]
# Printing the first three lines of the dataframe
print(combined_df.iloc[0:3,:])


# QUESTION 2

# Printing the first 12 lines for the data frame
print(combined_df.iloc[:12,:])


# QUESTION 3


# Define the categories for reporting
categories = ["Food", "Shelter", "All-items excluding food and energy"]

# Filter the dataset for the relevant items
filtered_data = combined_df[combined_df["Item"].isin(categories)]

# Pivot to reshape the data for percentage change calculation
pivot_data = filtered_data.pivot_table(index=["Jurisdiction", "Item"], columns="Month", values="CPI")

# Ensure the columns are in the correct order from Jan to Dec
# Extract the month order
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Extract unique years from the column names
years = sorted(set(col.split("-")[1] for col in pivot_data.columns))

# Create a properly ordered column list
ordered_columns = [f"{month}-{year}" for year in years for month in month_order if f"{month}-{year}" in pivot_data.columns]

# Reorder the pivot table
pivot_data = pivot_data[ordered_columns]

# Compute the month-to-month percentage change
month_to_month_change = round(pivot_data.pct_change(axis=1) * 100,1)

# Compute the average percentage change for each jurisdiction and category
avg_monthly_change = month_to_month_change.mean(axis=1).reset_index()

# Renaming columns
avg_monthly_change.columns = ["Jurisdiction", "Item", "Avg_Monthly_Change (%)"]

# Format the percentage change to one decimal place
avg_monthly_change["Avg_Monthly_Change (%)"] = avg_monthly_change["Avg_Monthly_Change (%)"].round(1)
print(avg_monthly_change)


#QUESTION 4

#Find the province which experience the highest average change in the each of the category
max_records = avg_monthly_change.loc[avg_monthly_change.groupby("Item")["Avg_Monthly_Change (%)"].idxmax()]
print(max_records)


#QUESTION 5

# Pivot to reshape the data for annual change in CPI for all services
pivot_data = combined_df.pivot_table(index=["Jurisdiction", "Item"], columns="Month", values="CPI")

# Calculate the annual change for each services
pivot_data["Annual_Change"] = ((pivot_data["Dec-24"]-pivot_data["Jan-24"])/pivot_data["Jan-24"] * 100).round(2)

# Calculate the average annual change of services for each jurisdiction
average_annual_change = round(pivot_data.groupby("Jurisdiction")["Annual_Change"].mean().reset_index(),1)
average_annual_change

print(average_annual_change)
      
      
# QUESTION 6

print(average_annual_change.loc[average_annual_change["Annual_Change"].idxmax()])