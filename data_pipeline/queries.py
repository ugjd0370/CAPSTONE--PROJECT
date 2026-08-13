import sqlite3
import pandas as pd
conn = sqlite3.connect("books.db")
queries = [
("Query 1",
"SELECT * FROM books WHERE rating=5;"),

("Query 2",
"SELECT * FROM books ORDER BY price_gbp DESC;"),

("Query 3",
"SELECT * FROM books LIMIT 10;"),

("Query 4",
"SELECT DISTINCT category_name FROM categories;"),

("Query 5",
"""
SELECT
b.title,
c.category_name,
b.rating
FROM books b
JOIN categories c
ON b.category_id=c.category_id;
""")
]

for name, sql in queries:
    print("="*50)
    print(name)
    df = pd.read_sql(sql, conn)
    print(df)
books_df = pd.read_sql(
    "SELECT * FROM books",
    conn
)
categories_df = pd.read_sql(
    "SELECT * FROM categories",
    conn
)
merged = pd.merge(
    books_df,
    categories_df,
    on="category_id"
)

print("\nResult using pd.merge():")
print(merged.head())
conn.close()