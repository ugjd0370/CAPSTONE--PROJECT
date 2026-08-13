import pandas as pd

df = pd.read_csv("books_raw.csv")

# Remove £ and convert to float
df["price_gbp"] = (
    df["price"]
    .str.replace("Â£", "", regex=False)
    .str.replace("�", "", regex=False)
    .astype(float)
)

# Rating mapping
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["rating"] = df["rating"].map(rating_map)

# Availability
df["in_stock"] = df["availability"].str.contains("In stock")

# INR conversion
RATE = 105.50

df["price_inr"] = df["price_gbp"] * RATE

# Fill missing numeric values
df["price_gbp"] = df["price_gbp"].fillna(df["price_gbp"].median())
df["rating"] = df["rating"].fillna(df["rating"].median())

# Save cleaned data
df.to_csv("books_clean.csv", index=False)

print(df.head())

print("Clean data saved successfully.")