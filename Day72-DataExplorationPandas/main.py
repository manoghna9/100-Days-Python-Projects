import pandas as pd

# Read the CSV file
df = pd.read_csv("salaries_by_college_major.csv")

# Display the first five rows
print(df.head())

# Number of rows and columns
print("\nShape:")
print(df.shape)

# Column names
print("\nColumns:")
print(df.columns)

# Check for missing values
print("\nMissing values:")
print(df.isna())

# Remove rows with missing values
clean_df = df.dropna()

# Information about the cleaned DataFrame
print("\nData Information:")
print(clean_df.info())

# Highest starting salary
print("\nHighest Starting Salary:")
print(clean_df["Starting Median Salary"].max())

print("\nMajor with Highest Starting Salary:")
print(clean_df.loc[clean_df["Starting Median Salary"].idxmax()])

# Highest mid-career salary
print("\nHighest Mid-Career Salary:")
print(clean_df["Mid-Career Median Salary"].max())

print("\nMajor with Highest Mid-Career Salary:")
print(clean_df.loc[clean_df["Mid-Career Median Salary"].idxmax()])

# Lowest starting salary
print("\nLowest Starting Salary:")
print(clean_df["Starting Median Salary"].min())

print("\nMajor with Lowest Starting Salary:")
print(clean_df.loc[clean_df["Starting Median Salary"].idxmin()])

# Lowest 10% risk (smallest spread)
clean_df["Spread"] = (
    clean_df["Mid-Career 90th Percentile Salary"]
    - clean_df["Mid-Career 10th Percentile Salary"]
)

print("\nLowest Risk Majors:")
print(clean_df.sort_values("Spread").head())

# Highest earning potential
print("\nHighest Earning Potential:")
print(
    clean_df.sort_values(
        "Mid-Career 90th Percentile Salary",
        ascending=False
    ).head()
)

# Highest salary spread
print("\nHighest Salary Spread:")
print(
    clean_df.sort_values(
        "Spread",
        ascending=False
    ).head()
)