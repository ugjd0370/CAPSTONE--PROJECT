# Module 1 — Data Pipeline

## 1. Project Overview

This module demonstrates a complete data pipeline:
**Scrape → Clean → Convert → Store → Query → Analyze**
The project collects book data from the public scraping-practice website:

https://books.toscrape.com/

The scraped data is cleaned, converted into proper data types, enriched with a fixed GBP-to-INR conversion rate, stored in a normalized SQLite database, and queried using SQL and pandas.

## 2. Data Source

Website:

https://books.toscrape.com/

Books to Scrape is a public website designed specifically for practicing web scraping.
No login, API key, or paid service is required.
The pipeline collects the following fields:

- `title`
- `price`
- `rating`
- `availability`
- `category`

The final raw dataset contains:

- 100 books
- 29 categories

The required minimum was 60 books across at least 3 categories.

Therefore, the project exceeds the minimum requirement.

---

## 3. Pipeline Flow

The complete workflow is:

```text
Books to Scrape
       |
       v
scrape_books.py
       |
       v
books_raw.csv
       |
       v
clean.py
       |
       v
books_clean.csv
       |
       v
database.py
       |
       v
books.db
       |
       v
queries.py
       |
       +---- SQL queries
       |
       +---- pandas read_sql()
       |
       +---- pandas merge()
4. Project Files
data_pipeline/
│
├── scrape_books.py
├── clean.py
├── database.py
├── queries.py
├── books_raw.csv
├── books_clean.csv
├── books.db
├── requirements.txt
└── README.md
File descriptions
scrape_books.py

Scrapes book information from Books to Scrape using:

requests
BeautifulSoup

It collects:
title
price
rating
availability
category

The raw results are saved to:
books_raw.csv
clean.py
Cleans and transforms the raw scraped data.

It:
converts price to numeric GBP
converts star ratings from text to integers
converts availability to Boolean values
calculates INR price
handles invalid or missing values
saves the cleaned dataset

Output:
books_clean.csv
database.py

Creates the SQLite database:
books.db
It creates two normalized tables:

categories
books
The tables are connected using a primary key and foreign key.

queries.py
Runs SQL queries against the SQLite database.
The queries demonstrate:
SELECT
WHERE
ORDER BY
LIMIT
DISTINCT
BETWEEN
JOIN
The script also demonstrates reading SQL results into pandas.

5. Installation
Make sure Python is installed.
A virtual environment can be used for the project.
Activate the virtual environment and install the required packages:
python -m pip install requests beautifulsoup4 pandas
Or install all dependencies using:
python -m pip install -r requirements.txt

Required Python libraries:
requests
beautifulsoup4
pandas
SQLite is provided through Python's built-in sqlite3 module, so a separate SQLite installation is not required for the Python script.

6. Running the Pipeline
Run the scripts in the following order.
Step 1 — Scrape the data
python scrape_books.py
This creates:
books_raw.csv
Expected result:
Status code: 200
Books found: 20

Raw data saved successfully to books_raw.csv

The final dataset contains:

Rows: 100
Categories: 29
Step 2 — Clean the data

Run:

python clean.py

Expected output includes:

Raw data:
Number of raw rows: 100

The cleaned dataset contains:

title
price_gbp
price_inr
rating
in_stock
category

Expected data types:

title         str
price_gbp     float64
price_inr     float64
rating        int64
in_stock      bool
category      str

The cleaned data is saved to:

books_clean.csv
Step 3 — Create the SQLite database

Run:

python database.py
This creates:
books.db
Expected output:

============================================================
DATABASE CREATED SUCCESSFULLY
============================================================

Categories: 29
Books: 100
Step 4 — Run SQL queries

Run:

python queries.py

This executes the required SQL queries and displays their results.
7. Fixed Currency Conversion
The assignment requires the following fixed conversion rate:
1 GBP = 105.50 INR

This is a project-defined fixed baseline.
It is:
not a live exchange rate
not a historical exchange rate
not retrieved from an API
not dependent on the current market rate
The calculation is:
price_inr = price_gbp × 105.50
Example:
price_gbp = 51.77
price_inr = 51.77 × 105.50
price_inr = 5461.735

8. Data Cleaning Decisions
8.1 Price
The website provides the price with the GBP currency symbol.
Example:
£51.77
The currency symbol is removed and the value is converted to a float.
Result:
51.77

Stored column:
price_gbp
Data type:
float

Examples:

One
Two
Three
Four
Five

They are converted to integers:
One   → 1
Two   → 2
Three → 3
Four  → 4
Five  → 5

Stored column:
rating
Data type:
integer

8.3 Availability
The website provides availability as text.
Example:
In stock
This is converted to:
True
Stored column:
in_stock
Data type:
boolean

When stored in SQLite, Boolean values are represented as:
1 = True
0 = False
8.4 Missing or Invalid Values

The pipeline is designed to avoid crashing when unexpected data is encountered.
For numeric fields, median imputation can be used when an invalid value is encountered.
If a row cannot be safely parsed and the required information cannot be recovered, the row may be dropped.
The cleaning script handles the data before loading it into the database.

The final cleaned dataset contains:
100 rows
and the required fields contain no missing values.

9. Database Design
The SQLite database is normalized into two related tables.
Categories table
categories
-------------------------
category_id      PRIMARY KEY
category_name    UNIQUE
Books table
books
-------------------------
book_id          PRIMARY KEY
title
price_gbp
price_inr
rating
in_stock
category_id      FOREIGN KEY
Relationship
categories
    |
    | category_id
    |
    v
books.category_id
The category_id foreign key connects each book to its category.
This avoids repeatedly storing the category name for every book and provides a normalized relational structure.

10. Database Results
The database contains:
Categories: 29
Books: 100

Example records:
(1, 'A Light in the Attic', 51.77, 3, 1, 'Poetry')
(2, 'Tipping the Velvet', 53.74, 1, 1, 'Historical Fiction')
(3, 'Soumission', 50.10, 1, 1, 'Fiction')
(4, 'Sharp Objects', 47.82, 4, 1, 'Mystery')
(5, 'Sapiens: A Brief History of Humankind', 54.23, 5, 1, 'History')
11. SQL Queries

The project demonstrates the required SQL operations.
Query 1 — SELECT and WHERE
SELECT title, price_gbp
FROM books
WHERE price_gbp > 30;
Explanation

This selects books whose GBP price is greater than 30.

This demonstrates:
SELECT
WHERE
12. Query 2 — ORDER BY
SELECT title, rating
FROM books
ORDER BY rating DESC;
Explanation
This sorts books from the highest rating to the lowest rating.
This demonstrates:

ORDER BY

13. Query 3 — LIMIT
SELECT title, price_gbp
FROM books
ORDER BY price_gbp DESC
LIMIT 10;
Explanation
This returns the 10 most expensive books.
This demonstrates:
LIMIT

14. Query 4 — DISTINCT
SELECT DISTINCT category_name
FROM categories;
Explanation
This returns each category only once.
This demonstrates:
DISTINCT

15. Query 5 — BETWEEN
SELECT title, price_gbp
FROM books
WHERE price_gbp BETWEEN 10 AND 30;
Explanation
This returns books with a price between £10 and £30.
This demonstrates:
BETWEEN

16. Query 6 — JOIN
SELECT
    b.title,
    b.rating,
    c.category_name
FROM books b
JOIN categories c
    ON b.category_id = c.category_id;
Explanation
The books table contains category_id.
The categories table contains:
category_id
category_name
The JOIN connects the two tables and displays the book title, rating, and category name.
This demonstrates:
JOIN

17. Pandas read_sql()
The project reads SQL query results into pandas DataFrames using:
pd.read_sql()
Example:
df_sql = pd.read_sql(query, connection)
print(df_sql)
This allows SQL query results to be analyzed using pandas.
At least two SQL query results are read into pandas DataFrames.

18. Pandas merge()
The JOIN result is also reproduced without SQL.
The two in-memory DataFrames are merged using:
pd.merge()
Example:
merged_df = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)
The result is compared with the SQL JOIN result.
The purpose is to demonstrate that the relational JOIN can also be reproduced using pandas.

19. SQL JOIN vs Pandas Merge
SQL approach:
SELECT
    b.title,
    b.rating,
    c.category_name
FROM books b
JOIN categories c
    ON b.category_id = c.category_id;

Pandas approach:
pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)

Both approaches produce equivalent relational results.

20. Requirements
The project requirements are stored in:
requirements.txt
The main packages are:
requests
beautifulsoup4
pandas

21. Reproducibility
The pipeline can be recreated from the source website by running:
python scrape_books.py
python clean.py
python database.py
python queries.py
This means the database and CSV files can be regenerated from the scraping and processing scripts.