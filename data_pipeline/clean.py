import pandas as pd


# ============================================================
# DATA CLEANING
# ============================================================

# Required fixed conversion rate from the assignment
GBP_TO_INR = 105.50


# ------------------------------------------------------------
# 1. Read the raw CSV file
# ------------------------------------------------------------

df = pd.read_csv("books_raw.csv")

print("Raw data:")
print(df.head())

print()
print("Number of raw rows:", len(df))


# ------------------------------------------------------------
# 2. Clean price
# ------------------------------------------------------------


df["price_gbp"] = (
    df["price"]
    .astype(str)
    .str.replace("Â", "", regex=False)
    .str.replace("£", "", regex=False)
    .str.strip()
)

df["price_gbp"] = pd.to_numeric(
    df["price_gbp"],
    errors="coerce"
)


# ------------------------------------------------------------
# 3. Clean star rating
# ------------------------------------------------------------
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["rating"] = df["rating"].map(rating_map)


# ------------------------------------------------------------
# 4. Clean availability
# ------------------------------------------------------------

df["in_stock"] = (
    df["availability"]
    .astype(str)
    .str.contains(
        "In stock",
        case=False,
        na=False
    )
)


# ------------------------------------------------------------
# 5. Handle invalid numeric values
# ------------------------------------------------------------
# If price or rating could not be converted,
# use the median value as required by the assignment.
# ------------------------------------------------------------

df["price_gbp"] = df["price_gbp"].fillna(
    df["price_gbp"].median()
)

df["rating"] = df["rating"].fillna(
    df["rating"].median()
)


#------------------------------------------------------------
# 6. Convert rating to integer
# ------------------------------------------------------------

df["rating"] = df["rating"].round().astype(int)


# ------------------------------------------------------------
# 7. Calculate INR price
# ------------------------------------------------------------
# Required project-defined rate:
#
# 1 GBP = 105.50 INR
# ------------------------------------------------------------

df["price_inr"] = df["price_gbp"] * GBP_TO_INR


# ------------------------------------------------------------
# 8. Keep only the required columns
# ------------------------------------------------------------

df = df[
    [
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category"
    ]
]


# ------------------------------------------------------------
# 9. Display cleaned data
# ------------------------------------------------------------

print()
print("=" * 60)
print("CLEANED DATA")
print("=" * 60)

print(df.head())


# ------------------------------------------------------------
# 10. Check data types
# ------------------------------------------------------------

print()
print("=" * 60)
print("DATA TYPES")
print("=" * 60)

print(df.dtypes)


# ------------------------------------------------------------
# 11. Check missing values
# ------------------------------------------------------------

print()
print("=" * 60)
print("MISSING VALUES")
print("=" * 60)

print(df.isnull().sum())


# ------------------------------------------------------------
# 12. Save cleaned CSV
# ------------------------------------------------------------

df.to_csv(
    "books_clean.csv",
    index=False
)

print()
print("Cleaned data saved successfully to books_clean.csv")

print()
print("Final number of rows:", len(df))

print()
print("Conversion rate used:")
print("1 GBP = 105.50 INR")