import sqlite3
import pandas as pd


# ============================================================
# SQL QUERIES + PANDAS ANALYSIS
# ============================================================

DB_NAME = "books.db"
# ------------------------------------------------------------
# 1. Connect to database
# ------------------------------------------------------------

connection = sqlite3.connect(DB_NAME)

print("=" * 70)
print("CONNECTED TO DATABASE")
print("=" * 70)
# ============================================================
# QUERY 1
# SELECT + WHERE
# ============================================================

query1 = """
SELECT
    title,
    price_gbp,
    rating
FROM books
WHERE rating >= 4;
"""

print()
print("=" * 70)
print("QUERY 1 - SELECT + WHERE")
print("=" * 70)

print(query1)

result1 = pd.read_sql(query1, connection)

print(result1.head(10))


# ============================================================
# QUERY 2
# ORDER BY
# ============================================================

query2 = """
SELECT
    title,
    price_gbp
FROM books
ORDER BY price_gbp DESC;
"""

print()
print("=" * 70)
print("QUERY 2 - ORDER BY")
print("=" * 70)

print(query2)

result2 = pd.read_sql(query2, connection)

print(result2.head(10))


# ============================================================
# QUERY 3
# LIMIT
# ============================================================

query3 = """
SELECT
    title,
    price_gbp
FROM books
LIMIT 10;
"""

print()
print("=" * 70)
print("QUERY 3 - LIMIT")
print("=" * 70)

print(query3)

result3 = pd.read_sql(query3, connection)

print(result3)


# ============================================================
# QUERY 4
# DISTINCT
# ============================================================

query4 = """
SELECT DISTINCT category_name
FROM categories
ORDER BY category_name;
"""

print()
print("=" * 70)
print("QUERY 4 - DISTINCT")
print("=" * 70)

print(query4)

result4 = pd.read_sql(query4, connection)

print(result4)


# ============================================================
# QUERY 5
# BETWEEN
# ============================================================

query5 = """
SELECT
    title,
    price_gbp,
    rating
FROM books
WHERE price_gbp BETWEEN 20 AND 40
ORDER BY price_gbp;
"""

print()
print("=" * 70)
print("QUERY 5 - BETWEEN")
print("=" * 70)

print(query5)

result5 = pd.read_sql(query5, connection)

print(result5.head(10))


# ============================================================
# QUERY 6
# JOIN
# ============================================================

query6 = """
SELECT
    books.title,
    books.price_gbp,
    books.rating,
    books.in_stock,
    categories.category_name
FROM books
JOIN categories
    ON books.category_id = categories.category_id
ORDER BY books.rating DESC, books.price_gbp DESC
LIMIT 10;
"""

print()
print("=" * 70)
print("QUERY 6 - JOIN")
print("=" * 70)

print(query6)

join_sql_result = pd.read_sql(query6, connection)

print(join_sql_result)


# ============================================================
# PANDAS - READ DATABASE TABLES
# ============================================================

print()
print("=" * 70)
print("READING TABLES INTO PANDAS")
print("=" * 70)


books_df = pd.read_sql(
    "SELECT * FROM books;",
    connection
)

categories_df = pd.read_sql(
    "SELECT * FROM categories;",
    connection
)

print()
print("Books DataFrame:")
print(books_df.head())

print()
print("Categories DataFrame:")
print(categories_df.head())


# ============================================================
# PANDAS MERGE
# ============================================================

print()
print("=" * 70)
print("PANDAS MERGE - REPRODUCING JOIN")
print("=" * 70)


# Merge books and categories using category_id

merge_result = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)

# Select the same columns as the SQL JOIN

merge_result = merge_result[
    [
        "title",
        "price_gbp",
        "rating",
        "in_stock",
        "category_name"
    ]
]

# Same sorting and LIMIT as SQL query

merge_result = merge_result.sort_values(
    by=["rating", "price_gbp"],
    ascending=[False, False]
).head(10)


merge_result = merge_result.reset_index(drop=True)

join_sql_result = join_sql_result.reset_index(drop=True)


print()
print("SQL JOIN RESULT:")
print(join_sql_result)


print()
print("PANDAS MERGE RESULT:")
print(merge_result)


# ============================================================
# COMPARE SQL JOIN AND PANDAS MERGE
# ============================================================

sql_compare = join_sql_result.copy()
pandas_compare = merge_result.copy()

sql_compare["price_gbp"] = sql_compare["price_gbp"].round(2)
pandas_compare["price_gbp"] = pandas_compare["price_gbp"].round(2)


same_result = sql_compare.equals(pandas_compare)


print()
print("=" * 70)
print("RESULT COMPARISON")
print("=" * 70)

print("SQL JOIN and pandas.merge produce equivalent results:", same_result)


# ============================================================
# CLOSE DATABASE
# ============================================================

connection.close()

print()
print("=" * 70)
print("DATABASE CONNECTION CLOSED")
print("=" * 70)