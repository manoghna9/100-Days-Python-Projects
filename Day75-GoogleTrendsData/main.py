"""
DAY 75
Time Series Analysis with Pandas and Matplotlib

In this project we will learn

• Reading CSV files
• Exploring datasets
• Cleaning data
• Working with datetime
• Resampling data
• Plotting multiple graphs
"""

# -----------------------------
# IMPORT LIBRARIES
# -----------------------------

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Make graphs look nicer
plt.style.use("ggplot")

# -----------------------------
# LOAD DATASETS
# -----------------------------

tesla = pd.read_csv("data/TESLA Search Trend vs Price.csv")
bitcoin = pd.read_csv("data/Daily Bitcoin Price.csv")
unemployment = pd.read_csv("data/UE Benefits Search vs UE Rate 2004-20.csv")

print("=" * 70)
print("DATASETS LOADED SUCCESSFULLY")
print("=" * 70)

# ----------------------------------------------------
# EXPLORE TESLA DATA
# ----------------------------------------------------

print("\nTESLA DATA")
print("-" * 40)

print(tesla.head())

print("\nShape:")
print(tesla.shape)

print("\nColumns:")
print(tesla.columns)

print("\nInformation")
print(tesla.info())

print("\nStatistics")
print(tesla.describe())

print("\nMissing Values")
print(tesla.isna().sum())

# ----------------------------------------------------
# EXPLORE BITCOIN DATA
# ----------------------------------------------------

print("\nBITCOIN DATA")
print("-" * 40)

print(bitcoin.head())

print("\nShape")
print(bitcoin.shape)

print("\nInformation")
print(bitcoin.info())

print("\nMissing Values")
print(bitcoin.isna().sum())

# ----------------------------------------------------
# EXPLORE UNEMPLOYMENT DATA
# ----------------------------------------------------

print("\nUNEMPLOYMENT DATA")
print("-" * 40)

print(unemployment.head())

print("\nShape")
print(unemployment.shape)

print("\nInformation")
print(unemployment.info())

print("\nMissing Values")
print(unemployment.isna().sum())

# ====================================================
# DATA CLEANING
# ====================================================

print("\n")
print("=" * 70)
print("DATA CLEANING")
print("=" * 70)

# Convert date columns into datetime objects

tesla["MONTH"] = pd.to_datetime(tesla["MONTH"])

bitcoin["DATE"] = pd.to_datetime(bitcoin["DATE"])

unemployment["MONTH"] = pd.to_datetime(unemployment["MONTH"])

# Set datetime as index

tesla.set_index("MONTH", inplace=True)

bitcoin.set_index("DATE", inplace=True)

unemployment.set_index("MONTH", inplace=True)

print("\nDatetime conversion successful!")

print("\nTesla Index")
print(type(tesla.index))

print("\nBitcoin Index")
print(type(bitcoin.index))

print("\nUnemployment Index")
print(type(unemployment.index))

# ====================================================
# RESAMPLING
# ====================================================

print("\n")
print("=" * 70)
print("MONTHLY BITCOIN DATA")
print("=" * 70)

bitcoin_monthly = bitcoin.resample("M").mean()

print(bitcoin_monthly.head())

# ====================================================
# REMOVE MISSING VALUES
# ====================================================

tesla.dropna(inplace=True)
bitcoin.dropna(inplace=True)
bitcoin_monthly.dropna(inplace=True)
unemployment.dropna(inplace=True)

print("\nAll missing values removed!")

# ====================================================
# DATA IS READY
# ====================================================

print("\n")
print("=" * 70)
print("DATA CLEANING COMPLETE")
print("=" * 70)

print("\nTesla")
print(tesla.head())

print("\nBitcoin Monthly")
print(bitcoin_monthly.head())

print("\nUnemployment")
print(unemployment.head())
# ====================================================
# TESLA SEARCH TREND VS STOCK PRICE
# ====================================================

print("\nCreating Tesla Visualization...")

# Create a new figure and axis
fig, ax1 = plt.subplots(figsize=(15, 7))

# ----------------------------------------------------
# LEFT Y-AXIS (Google Searches)
# ----------------------------------------------------

ax1.set_title(
    "Tesla Google Search Interest vs Stock Price",
    fontsize=18,
    pad=20
)

ax1.set_xlabel("Year", fontsize=12)

ax1.set_ylabel(
    "Google Search Interest",
    color="tab:blue",
    fontsize=12
)

ax1.plot(
    tesla.index,
    tesla["TSLA_WEB_SEARCH"],
    color="tab:blue",
    linewidth=2,
    label="Google Searches"
)

# Make left axis labels blue
ax1.tick_params(axis="y", labelcolor="tab:blue")

# ----------------------------------------------------
# RIGHT Y-AXIS (Stock Price)
# ----------------------------------------------------

ax2 = ax1.twinx()

ax2.set_ylabel(
    "Tesla Stock Price ($)",
    color="tab:red",
    fontsize=12
)

ax2.plot(
    tesla.index,
    tesla["TSLA_USD_CLOSE"],
    color="tab:red",
    linewidth=2,
    label="Stock Price"
)

ax2.tick_params(axis="y", labelcolor="tab:red")

# ----------------------------------------------------
# FORMAT THE DATE AXIS
# ----------------------------------------------------

year_locator = mdates.YearLocator()

year_formatter = mdates.DateFormatter("%Y")

ax1.xaxis.set_major_locator(year_locator)

ax1.xaxis.set_major_formatter(year_formatter)

# Rotate dates for readability
plt.xticks(rotation=45)

# ----------------------------------------------------
# GRID
# ----------------------------------------------------

ax1.grid(
    True,
    linestyle="--",
    alpha=0.4
)

# ----------------------------------------------------
# LEGENDS
# ----------------------------------------------------

line1, label1 = ax1.get_legend_handles_labels()

line2, label2 = ax2.get_legend_handles_labels()

ax1.legend(
    line1 + line2,
    label1 + label2,
    loc="upper left"
)

# ----------------------------------------------------
# REMOVE EXTRA WHITESPACE
# ----------------------------------------------------

plt.tight_layout()

# ----------------------------------------------------
# DISPLAY GRAPH
# ----------------------------------------------------

plt.show()
# ====================================================
# BITCOIN ANALYSIS
# ====================================================

print("\nCreating Bitcoin Visualization...")

# ----------------------------------------------------
# CREATE A NEW FIGURE
# ----------------------------------------------------

fig, ax = plt.subplots(figsize=(15, 7))

# ----------------------------------------------------
# PLOT DAILY BITCOIN PRICE
# ----------------------------------------------------

ax.plot(
    bitcoin.index,
    bitcoin["CLOSE"],
    color="orange",
    linewidth=0.8,
    alpha=0.35,
    label="Daily Price"
)

# ----------------------------------------------------
# PLOT MONTHLY AVERAGE PRICE
# ----------------------------------------------------

ax.plot(
    bitcoin_monthly.index,
    bitcoin_monthly["CLOSE"],
    color="darkgreen",
    linewidth=2.5,
    marker="o",
    markersize=5,
    label="Monthly Average"
)

# ----------------------------------------------------
# TITLE AND LABELS
# ----------------------------------------------------

ax.set_title(
    "Bitcoin Daily Price vs Monthly Average",
    fontsize=18,
    pad=20
)

ax.set_xlabel(
    "Year",
    fontsize=12
)

ax.set_ylabel(
    "Bitcoin Price (USD)",
    fontsize=12
)

# ----------------------------------------------------
# FORMAT DATES
# ----------------------------------------------------

year_locator = mdates.YearLocator()

year_formatter = mdates.DateFormatter("%Y")

ax.xaxis.set_major_locator(year_locator)

ax.xaxis.set_major_formatter(year_formatter)

plt.xticks(rotation=45)

# ----------------------------------------------------
# GRID
# ----------------------------------------------------

ax.grid(
    True,
    linestyle="--",
    alpha=0.4
)

# ----------------------------------------------------
# LEGEND
# ----------------------------------------------------

ax.legend()

# ----------------------------------------------------
# REMOVE EXTRA WHITESPACE
# ----------------------------------------------------

plt.tight_layout()

# ----------------------------------------------------
# DISPLAY GRAPH
# ----------------------------------------------------

plt.show()