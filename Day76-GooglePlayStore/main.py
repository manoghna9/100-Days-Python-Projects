"""
Day 76 - Google Play Store Data Analysis

An original implementation of the Day 76 project.

Topics covered:
- Data cleaning
- Missing values
- Duplicate removal
- Numeric type conversion
- Preliminary data exploration
- Plotly pie and donut charts
- Plotly bar charts
- Plotly scatter plots
- Extracting nested genre data using .stack()
- Grouped bar charts
- Box plots
- Bubble charts
- Free vs paid app analysis
"""

from pathlib import Path

import pandas as pd
import plotly.express as px


# ============================================================
# 1. SETTINGS
# ============================================================

DATA_FOLDER = Path("data")
OUTPUT_FOLDER = Path("output")

# The program will look for the CSV using these names.
POSSIBLE_FILES = [
    DATA_FOLDER / "apps.csv",
    DATA_FOLDER / "googleplaystore.csv",
    DATA_FOLDER / "Google-Playstore.csv",
    Path("apps.csv"),
    Path("googleplaystore.csv"),
]

TOP_N = 10


# ============================================================
# 2. FIND THE DATASET
# ============================================================

def find_dataset():
    """
    Look through the possible file locations and return
    the first CSV that exists.
    """

    for file in POSSIBLE_FILES:
        if file.exists():
            return file

    print("\nCould not find the Google Play Store CSV.")
    print("Put your CSV inside the 'data' folder.")
    print("The preferred filename is:")
    print("    apps.csv")

    raise FileNotFoundError("Google Play Store CSV not found.")


# ============================================================
# 3. LOAD THE DATA
# ============================================================

def load_data():
    """Load the Google Play Store dataset into pandas."""

    file_path = find_dataset()

    print("=" * 70)
    print("GOOGLE PLAY STORE DATA ANALYSIS")
    print("=" * 70)

    print(f"\nLoading dataset: {file_path}")

    df = pd.read_csv(file_path)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    return df


# ============================================================
# 4. INITIAL DATA EXPLORATION
# ============================================================

def inspect_data(df):
    """
    Look at the dataset before making any changes.
    """

    print("\n" + "=" * 70)
    print("INITIAL DATA EXPLORATION")
    print("=" * 70)

    print("\nFirst five rows:")
    print(df.head())

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nDataset information:")
    print(df.info())

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nNumber of duplicate rows:")
    print(df.duplicated().sum())


# ============================================================
# 5. CLEAN COLUMN NAMES
# ============================================================

def clean_column_names(df):
    """Remove accidental spaces around column names."""

    df = df.copy()

    df.columns = df.columns.str.strip()

    return df


# ============================================================
# 6. CLEAN RATING
# ============================================================

def clean_rating(df):
    """
    Convert Rating into a numeric column.

    Invalid values become NaN.
    """

    if "Rating" in df.columns:

        df["Rating"] = pd.to_numeric(
            df["Rating"],
            errors="coerce"
        )

    return df


# ============================================================
# 7. CLEAN REVIEWS
# ============================================================

def clean_reviews(df):
    """Convert Reviews into numeric values."""

    if "Reviews" in df.columns:

        df["Reviews"] = pd.to_numeric(
            df["Reviews"],
            errors="coerce"
        )

    return df


# ============================================================
# 8. CLEAN INSTALLS
# ============================================================

def clean_installs(df):
    """
    Convert values such as:

        1,000+
        10,000+
        1,000,000+

    into:

        1000
        10000
        1000000
    """

    if "Installs" in df.columns:

        df["Installs"] = (
            df["Installs"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("+", "", regex=False)
            .str.strip()
        )

        df["Installs"] = pd.to_numeric(
            df["Installs"],
            errors="coerce"
        )

    return df


# ============================================================
# 9. CLEAN PRICE
# ============================================================

def clean_price(df):
    """
    Convert:

        $4.99
        $0.99
        $10.00

    into:

        4.99
        0.99
        10.00
    """

    if "Price" in df.columns:

        df["Price"] = (
            df["Price"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.strip()
        )

        df["Price"] = pd.to_numeric(
            df["Price"],
            errors="coerce"
        )

    return df


# ============================================================
# 10. REMOVE MISSING VALUES
# ============================================================

def remove_missing_values(df):
    """
    Remove rows that don't have the information required
    for our analysis.
    """

    important_columns = [
        "App",
        "Category",
        "Rating",
        "Reviews",
        "Installs",
        "Type"
    ]

    # Only use columns that actually exist.
    important_columns = [
        column
        for column in important_columns
        if column in df.columns
    ]

    before = len(df)

    df = df.dropna(
        subset=important_columns
    )

    after = len(df)

    print("\nRows before removing NaN values:", before)
    print("Rows after removing NaN values:", after)
    print("Rows removed:", before - after)

    return df


# ============================================================
# 11. REMOVE DUPLICATES
# ============================================================

def remove_duplicates(df):
    """
    Remove duplicate applications.

    Keeping the first occurrence prevents the same app
    from being counted multiple times.
    """

    before = len(df)

    if "App" in df.columns:
        df = df.drop_duplicates(
            subset="App",
            keep="first"
        )
    else:
        df = df.drop_duplicates()

    after = len(df)

    print("\nRows before removing duplicates:", before)
    print("Rows after removing duplicates:", after)
    print("Duplicates removed:", before - after)

    return df.reset_index(drop=True)


# ============================================================
# 12. COMPLETE CLEANING PIPELINE
# ============================================================

def clean_data(df):

    print("\n" + "=" * 70)
    print("DATA CLEANING")
    print("=" * 70)

    df = clean_column_names(df)

    df = clean_rating(df)

    df = clean_reviews(df)

    df = clean_installs(df)

    df = clean_price(df)

    # A missing Price normally means that the value wasn't
    # available. For the free/paid analysis we treat it as 0.
    if "Price" in df.columns:
        df["Price"] = df["Price"].fillna(0)

    df = remove_missing_values(df)

    df = remove_duplicates(df)

    print("\nCleaning complete.")

    print("\nCleaned data types:")
    print(df.dtypes)

    return df


# ============================================================
# 13. PRELIMINARY EXPLORATION
# ============================================================

def preliminary_exploration(df):

    print("\n" + "=" * 70)
    print("PRELIMINARY EXPLORATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Highest rated apps
    # --------------------------------------------------------

    highest_rating = df["Rating"].max()

    print("\nHighest rating:", highest_rating)

    highest_rated = df[
        df["Rating"] == highest_rating
    ][["App", "Rating"]]

    print("\nHighest-rated apps:")
    print(
        highest_rated
        .head(TOP_N)
        .to_string(index=False)
    )

    # --------------------------------------------------------
    # Most reviewed apps
    # --------------------------------------------------------

    print("\nMost reviewed apps:")

    most_reviewed = df.nlargest(
        TOP_N,
        "Reviews"
    )[["App", "Reviews"]]

    print(
        most_reviewed
        .to_string(index=False)
    )

    # --------------------------------------------------------
    # Most installed apps
    # --------------------------------------------------------

    print("\nMost installed apps:")

    most_installed = df.nlargest(
        TOP_N,
        "Installs"
    )[["App", "Installs"]]

    print(
        most_installed
        .to_string(index=False)
    )

    # --------------------------------------------------------
    # Most expensive apps
    # --------------------------------------------------------

    print("\nMost expensive apps:")

    paid_apps = df[
        df["Price"] > 0
    ]

    most_expensive = paid_apps.nlargest(
        TOP_N,
        "Price"
    )[["App", "Price"]]

    print(
        most_expensive
        .to_string(index=False)
    )


# ============================================================
# 14. CATEGORY COUNTS
# ============================================================

def category_counts(df):

    print("\n" + "=" * 70)
    print("APP COUNT BY CATEGORY")
    print("=" * 70)

    counts = df["Category"].value_counts()

    print(counts.to_string())

    return counts


# ============================================================
# 15. PLOTLY HELPER
# ============================================================

def display_chart(fig, filename):

    """
    Apply a consistent layout to the Plotly chart.

    The chart is also saved as an HTML file so you can
    open it later in a browser.
    """

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        margin=dict(
            l=50,
            r=50,
            t=80,
            b=50
        )
    )

    output_file = OUTPUT_FOLDER / filename

    fig.write_html(output_file)

    print(
        f"\nChart saved to: {output_file}"
    )

    fig.show()


# ============================================================
# 16. PIE CHART
# ============================================================

def category_pie_chart(df):

    counts = (
        df["Category"]
        .value_counts()
        .reset_index()
    )

    counts.columns = [
        "Category",
        "App Count"
    ]

    fig = px.pie(
        counts,
        names="Category",
        values="App Count",
        title="Apps by Category"
    )

    display_chart(
        fig,
        "01_category_pie.html"
    )


# ============================================================
# 17. DONUT CHART
# ============================================================

def category_donut_chart(df):

    counts = (
        df["Category"]
        .value_counts()
        .reset_index()
    )

    counts.columns = [
        "Category",
        "App Count"
    ]

    fig = px.pie(
        counts,
        names="Category",
        values="App Count",
        hole=0.45,
        title="Google Play Store Categories"
    )

    display_chart(
        fig,
        "02_category_donut.html"
    )


# ============================================================
# 18. TOP CATEGORIES BY INSTALLS
# ============================================================

def category_install_chart(df):

    category_installs = (
        df
        .groupby("Category")["Installs"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(TOP_N)
        .reset_index()
    )

    fig = px.bar(
        category_installs,
        x="Category",
        y="Installs",
        text="Installs",
        title="Top Categories by Total Installs"
    )

    fig.update_traces(
        texttemplate="%{text:.3s}",
        textposition="outside"
    )

    display_chart(
        fig,
        "03_category_installs.html"
    )


# ============================================================
# 19. TOP CATEGORIES BY REVIEWS
# ============================================================

def category_review_chart(df):

    category_reviews = (
        df
        .groupby("Category")["Reviews"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(TOP_N)
        .reset_index()
    )

    fig = px.bar(
        category_reviews,
        x="Category",
        y="Reviews",
        text="Reviews",
        title="Top Categories by Total Reviews"
    )

    fig.update_traces(
        texttemplate="%{text:.3s}",
        textposition="outside"
    )

    display_chart(
        fig,
        "04_category_reviews.html"
    )


# ============================================================
# 20. FREE VS PAID
# ============================================================

def free_paid_chart(df):

    counts = (
        df["Type"]
        .value_counts()
        .reset_index()
    )

    counts.columns = [
        "Type",
        "App Count"
    ]

    fig = px.bar(
        counts,
        x="Type",
        y="App Count",
        color="Type",
        text="App Count",
        title="Free vs Paid Apps"
    )

    fig.update_traces(
        textposition="outside"
    )

    display_chart(
        fig,
        "05_free_vs_paid.html"
    )


# ============================================================
# 21. REVIEWS VS INSTALLS
# ============================================================

def reviews_vs_installs(df):

    plot_data = df[
        df["Reviews"] > 0
    ].copy()

    fig = px.scatter(
        plot_data,
        x="Reviews",
        y="Installs",
        color="Category",
        hover_name="App",
        log_x=True,
        log_y=True,
        opacity=0.65,
        title="Reviews vs Installs"
    )

    display_chart(
        fig,
        "06_reviews_vs_installs.html"
    )


# ============================================================
# 22. RATING VS REVIEWS
# ============================================================

def rating_vs_reviews(df):

    plot_data = df[
        df["Reviews"] > 0
    ].copy()

    fig = px.scatter(
        plot_data,
        x="Reviews",
        y="Rating",
        color="Type",
        hover_name="App",
        log_x=True,
        opacity=0.65,
        title="Rating vs Number of Reviews"
    )

    display_chart(
        fig,
        "07_rating_vs_reviews.html"
    )


# ============================================================
# 23. PRICE VS RATING
# ============================================================

def price_vs_rating(df):

    paid = df[
        df["Price"] > 0
    ].copy()

    if paid.empty:
        print("\nNo paid apps available.")
        return

    fig = px.scatter(
        paid,
        x="Price",
        y="Rating",
        color="Category",
        size="Reviews",
        hover_name="App",
        title="Price vs Rating for Paid Apps"
    )

    display_chart(
        fig,
        "08_price_vs_rating.html"
    )


# ============================================================
# 24. EXTRACT GENRES USING STACK()
# ============================================================

def extract_genres(df):

    """
    Some apps have multiple genres stored together.

    Example:

        Art & Design;Creativity

    We split that string into separate values and then
    use stack() to turn them into individual rows.
    """

    if "Genres" not in df.columns:
        print("\nGenres column does not exist.")
        return pd.DataFrame()

    genres = df[
        ["App", "Genres"]
    ].copy()

    # Convert a string such as:
    #
    # Art & Design;Creativity
    #
    # into:
    #
    # ["Art & Design", "Creativity"]

    genres["Genres"] = (
        genres["Genres"]
        .astype(str)
        .str.split(";")
    )

    # Turn each list into multiple columns.
    genres = (
        genres
        .set_index("App")["Genres"]
        .apply(pd.Series)
    )

    # stack() converts the columns into rows.
    genres = (
        genres
        .stack()
        .reset_index()
    )

    genres.columns = [
        "App",
        "Level",
        "Genre"
    ]

    return genres[
        ["App", "Genre"]
    ]


# ============================================================
# 25. GENRE ANALYSIS
# ============================================================

def genre_analysis(df):

    genre_data = extract_genres(df)

    if genre_data.empty:
        return

    print("\n" + "=" * 70)
    print("GENRE ANALYSIS")
    print("=" * 70)

    counts = (
        genre_data["Genre"]
        .value_counts()
        .reset_index()
    )

    counts.columns = [
        "Genre",
        "App Count"
    ]

    print("\nMost common genres:")

    print(
        counts
        .head(TOP_N)
        .to_string(index=False)
    )

    top_genres = counts.head(15)

    fig = px.bar(
        top_genres,
        x="App Count",
        y="Genre",
        orientation="h",
        title="Most Common App Genres"
    )

    display_chart(
        fig,
        "09_top_genres.html"
    )


# ============================================================
# 26. AVERAGE RATING: FREE VS PAID
# ============================================================

def average_rating_by_type(df):

    averages = (
        df
        .groupby("Type")["Rating"]
        .mean()
        .round(2)
        .reset_index()
    )

    print("\nAverage rating by app type:")
    print(
        averages
        .to_string(index=False)
    )

    fig = px.bar(
        averages,
        x="Type",
        y="Rating",
        color="Type",
        text="Rating",
        title="Average Rating: Free vs Paid"
    )

    fig.update_traces(
        textposition="outside"
    )

    display_chart(
        fig,
        "10_average_rating.html"
    )


# ============================================================
# 27. GROUPED BAR CHART
# ============================================================

def category_type_grouped_chart(df):

    counts = (
        df
        .groupby(
            ["Category", "Type"]
        )
        .size()
        .reset_index(
            name="App Count"
        )
    )

    popular_categories = (
        df["Category"]
        .value_counts()
        .head(10)
        .index
    )

    counts = counts[
        counts["Category"].isin(
            popular_categories
        )
    ]

    fig = px.bar(
        counts,
        x="Category",
        y="App Count",
        color="Type",
        barmode="group",
        title="Free vs Paid Apps by Category"
    )

    display_chart(
        fig,
        "11_grouped_category_type.html"
    )


# ============================================================
# 28. BOX PLOT
# ============================================================

def rating_box_plot(df):

    fig = px.box(
        df,
        x="Type",
        y="Rating",
        color="Type",
        points="outliers",
        title="Rating Distribution: Free vs Paid Apps"
    )

    display_chart(
        fig,
        "12_rating_box_plot.html"
    )


# ============================================================
# 29. CATEGORY BOX PLOT
# ============================================================

def category_rating_box_plot(df):

    popular_categories = (
        df["Category"]
        .value_counts()
        .head(10)
        .index
    )

    plot_data = df[
        df["Category"].isin(
            popular_categories
        )
    ].copy()

    fig = px.box(
        plot_data,
        x="Category",
        y="Rating",
        color="Category",
        title="Rating Distribution by Category"
    )

    fig.update_xaxes(
        tickangle=-35
    )

    display_chart(
        fig,
        "13_category_rating_box_plot.html"
    )


# ============================================================
# 30. BUBBLE CHART
# ============================================================

def bubble_chart(df):

    plot_data = df[
        df["Reviews"] > 0
    ].copy()

    fig = px.scatter(
        plot_data,
        x="Reviews",
        y="Rating",
        size="Installs",
        color="Type",
        hover_name="App",
        log_x=True,
        size_max=45,
        opacity=0.65,
        title="Ratings, Reviews and Installs"
    )

    display_chart(
        fig,
        "14_bubble_chart.html"
    )


# ============================================================
# 31. INTERPRETATION
# ============================================================

def interpretation(df):

    print("\n" + "=" * 70)
    print("DATA-DRIVEN INTERPRETATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Largest category by number of apps
    # --------------------------------------------------------

    category_count = (
        df["Category"]
        .value_counts()
    )

    largest_category = (
        category_count
        .idxmax()
    )

    number_of_apps = (
        category_count
        .max()
    )

    print(
        f"\n1. The category with the most apps is "
        f"{largest_category}, containing "
        f"{number_of_apps:,} apps."
    )

    # --------------------------------------------------------
    # Category with most installs
    # --------------------------------------------------------

    installs = (
        df
        .groupby("Category")["Installs"]
        .sum()
    )

    install_leader = installs.idxmax()

    install_value = installs.max()

    print(
        f"\n2. {install_leader} has the largest "
        f"total number of recorded installs: "
        f"{install_value:,.0f}."
    )

    # --------------------------------------------------------
    # Category with most reviews
    # --------------------------------------------------------

    reviews = (
        df
        .groupby("Category")["Reviews"]
        .sum()
    )

    review_leader = reviews.idxmax()

    print(
        f"\n3. {review_leader} has the largest "
        f"combined number of reviews."
    )

    # --------------------------------------------------------
    # Free vs paid
    # --------------------------------------------------------

    type_counts = (
        df["Type"]
        .value_counts()
    )

    print("\n4. Free vs paid apps:")

    for app_type, count in type_counts.items():

        print(
            f"   {app_type}: {count:,}"
        )

    # --------------------------------------------------------
    # Average ratings
    # --------------------------------------------------------

    ratings = (
        df
        .groupby("Type")["Rating"]
        .mean()
    )

    print("\n5. Average ratings:")

    for app_type, rating in ratings.items():

        print(
            f"   {app_type}: {rating:.2f}"
        )

    # --------------------------------------------------------
    # Most expensive app
    # --------------------------------------------------------

    paid = df[
        df["Price"] > 0
    ]

    if not paid.empty:

        expensive = paid.loc[
            paid["Price"].idxmax()
        ]

        print(
            f"\n6. Most expensive app: "
            f"{expensive['App']} "
            f"(${expensive['Price']:.2f})"
        )

    # --------------------------------------------------------
    # Important interpretation note
    # --------------------------------------------------------

    print(
        "\n7. Important statistical note:"
    )

    print(
        "   A relationship between two variables does not "
        "automatically mean that one caused the other."
    )

    print(
        "   For example, an app with many reviews will often "
        "also have many installs, but this does not prove that "
        "reviews alone caused the installs."
    )


# ============================================================
# 32. SAVE CLEANED DATA
# ============================================================

def save_cleaned_data(df):

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        OUTPUT_FOLDER /
        "cleaned_apps.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nCleaned dataset saved to:"
        f"\n{output_file}"
    )


# ============================================================
# 33. MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    df = load_data()

    # --------------------------------------------------------
    # Inspect raw dataset
    # --------------------------------------------------------

    inspect_data(df)

    # --------------------------------------------------------
    # Clean
    # --------------------------------------------------------

    df = clean_data(df)

    # --------------------------------------------------------
    # Explore
    # --------------------------------------------------------

    preliminary_exploration(df)

    category_counts(df)

    # --------------------------------------------------------
    # Plotly charts
    # --------------------------------------------------------

    category_pie_chart(df)

    category_donut_chart(df)

    category_install_chart(df)

    category_review_chart(df)

    free_paid_chart(df)

    reviews_vs_installs(df)

    rating_vs_reviews(df)

    price_vs_rating(df)

    # --------------------------------------------------------
    # Nested data / stack()
    # --------------------------------------------------------

    genre_analysis(df)

    # --------------------------------------------------------
    # Grouped comparisons
    # --------------------------------------------------------

    average_rating_by_type(df)

    category_type_grouped_chart(df)

    # --------------------------------------------------------
    # Box plots
    # --------------------------------------------------------

    rating_box_plot(df)

    category_rating_box_plot(df)

    # --------------------------------------------------------
    # Bubble chart
    # --------------------------------------------------------

    bubble_chart(df)

    # --------------------------------------------------------
    # Conclusions
    # --------------------------------------------------------

    interpretation(df)

    # --------------------------------------------------------
    # Save cleaned dataset
    # --------------------------------------------------------

    save_cleaned_data(df)

    print("\n" + "=" * 70)
    print("DAY 76 COMPLETE!")
    print("=" * 70)


# ============================================================
# 34. RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()