import sqlite3
import pandas as pd
df = pd.read_csv("books_clean.csv")
conn = sqlite3.connect("books.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories(
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock INTEGER,
    category_id INTEGER,
    FOREIGN KEY(category_id)
    REFERENCES categories(category_id)
)
""")

# Insert categories
categories = df["category"].unique()

for category in categories:
    cursor.execute(
        "INSERT OR IGNORE INTO categories(category_name) VALUES(?)",
        (category,)
    )
conn.commit()
category_ids = pd.read_sql(
    "SELECT * FROM categories",
    conn
)
merged = df.merge(
    category_ids,
    left_on="category",
    right_on="category_name"
)
for _, row in merged.iterrows():

    cursor.execute("""
    INSERT INTO books(
        title,
        price_gbp,
        price_inr,
        rating,
        in_stock,
        category_id
    )
    VALUES(?,?,?,?,?,?)
    """, (
        row["title"],
        row["price_gbp"],
        row["price_inr"],
        int(row["rating"]),
        int(row["in_stock"]),
        int(row["category_id"])
    ))
conn.commit()
print("Database created successfully.")
conn.close()