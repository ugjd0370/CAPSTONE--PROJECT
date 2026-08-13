import sqlite3
import pandas as pd


# ============================================================
# DATABASE CREATION
# ============================================================

# Database file
DB_NAME = "books.db"

# ------------------------------------------------------------
# 1. Read cleaned CSV
# ------------------------------------------------------------

df = pd.read_csv("books_clean.csv")

print("Cleaned data loaded.")
print("Number of books:", len(df))

# ------------------------------------------------------------
# 2. Connect to SQLite database
# ------------------------------------------------------------

connection = sqlite3.connect(DB_NAME)

cursor = connection.cursor()


# ------------------------------------------------------------
# 3. Enable foreign key support
# ------------------------------------------------------------

cursor.execute("PRAGMA foreign_keys = ON;")


# ------------------------------------------------------------
# 4. Create categories table
# ------------------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
);
""")


# ------------------------------------------------------------
# 5. Create books table
# ------------------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock INTEGER,
    category_id INTEGER,
    
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);
""")


# ------------------------------------------------------------
# 6. Insert categories
# ------------------------------------------------------------

categories = df["category"].drop_duplicates()


for category in categories:

    cursor.execute(
        """
        INSERT OR IGNORE INTO categories (category_name)
        VALUES (?);
        """,
        (category,)
    )


# ------------------------------------------------------------
# 7. Insert books
# ------------------------------------------------------------

for _, row in df.iterrows():

    # Find category ID
    cursor.execute(
        """
        SELECT category_id
        FROM categories
        WHERE category_name = ?;
        """,
        (row["category"],)
    )

    category_id = cursor.fetchone()[0]


    # Convert boolean to SQLite INTEGER
    in_stock = 1 if row["in_stock"] else 0


    # Insert book
    cursor.execute(
        """
        INSERT INTO books (
            title,
            price_gbp,
            price_inr,
            rating,
            in_stock,
            category_id
        )
        VALUES (?, ?, ?, ?, ?, ?);
        """,
        (
            row["title"],
            row["price_gbp"],
            row["price_inr"],
            row["rating"],
            in_stock,
            category_id
        )
    )


# ------------------------------------------------------------
# 8. Save changes
# ------------------------------------------------------------

connection.commit()

# ------------------------------------------------------------
# 9. Check number of records
# ------------------------------------------------------------

cursor.execute("SELECT COUNT(*) FROM categories;")

category_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM books;")

book_count = cursor.fetchone()[0]


print()
print("=" * 60)
print("DATABASE CREATED SUCCESSFULLY")
print("=" * 60)

print("Categories:", category_count)
print("Books:", book_count)

# ------------------------------------------------------------
# 10. Display sample books
# ------------------------------------------------------------

cursor.execute("""
SELECT
    books.book_id,
    books.title,
    books.price_gbp,
    books.rating,
    books.in_stock,
    categories.category_name
FROM books
JOIN categories
    ON books.category_id = categories.category_id
LIMIT 5;
""")


rows = cursor.fetchall()


print()
print("Sample books:")

for row in rows:
    print(row)


# ------------------------------------------------------------
# 11. Close database
# ------------------------------------------------------------

connection.close()

print()
print("Database connection closed.")
print("Database file:", DB_NAME)