# Data Pipeline Module

## 1. Project Overview
This module demOnstrates a complete data pipeline:
**Scrape → Clean → Convert → Store → Query → Analyze**
The project collects book data from the public practice website:
https://books.toscrape.com/

The scraped data is cleaned, converted into proper data types, enriched with a fixed GBP-to-INR conversion rate, stored in a normalized SQLite database, and queried using SQL and pandas.

## 2. Data Source
Website:
https://books.toscrape.com/
The website is designed specifically for practicing web scraping.
The project collects the following fields:

- `title`
- `price`
- `rating`
- `availability`
- `category`

---

## 3. Fixed Currency Conversion
The project uses the required fixed conversion rate:
**1 GBP = 105.50 INR**
This is a project-defined fixed rate.
It is not a live exchange rate and no currency API is used.
The INR price is calculated as:
```text
price_inr = price_gbp × 105.50

## 4.PROJECT FILES

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

## 5.scrape_books.py
Scrapes book information from Books to Scrape using:
requests
BeautifulSoup
It collects:
1.title
2.price
3.rating
4.availability
5.category
and saves the raw data.

## 6.clean.py
Cleans and transforms the scraped data.
It:
converts price to numeric GBP
converts star ratings from text to integers
converts availability to Boolean values
calculates INR price
handles invalid or missing values

## 7.database.py
Creates the SQLite database and normalized tables.
The database contains:
categories
books
The tables are connected using a primary key and foreign key.

## 8.queries.py
Runs SQL queries demonstrating:
SELECT
WHERE
ORDER BY
LIMIT
DISTINCT
BETWEEN / IN
JOIN
It also reads query results using pandas

## 9. Installation
Make sure Python is installed.
Create and activate a virtual environment if required.
Install the required packages:
pip install requests beautifulsoup4 pandas
Or install everything from requirements.txt:
pip install -r requirements.txt

## 10. Running the Pipeline
python scrape_books.py
Then run the cleaning script:
python clean.py
Then create and populate the database:
python database.py
Finally run the SQL queries:
python queries.py

## 11. Data Cleaning Decisions
Price
The original price contains the GBP currency symbol.
Example:
£45.17
It is converted to:
45.17
and stored as a floating-point value in price_gbp.

## 12.Rating
The website provides ratings as text such as:
One
Two
Three
Four
Five

These are converted to integers:
One   → 1
Two   → 2
Three → 3
Four  → 4
Five  → 5

## 13.Availability
Availability text is converted to Boolean values.
For example:
In stock → True

If an unexpected availability value is encountered, it is handled without crashing the pipeline.

Missing or Invalid Values

The pipeline is designed to handle unexpected or missing values.
For numeric fields, median imputation can be used when appropriate.
If a row cannot be safely parsed and is essential to the required fields, the row can be dropped rather than allowing the pipeline to fail.
The chosen handling approach is documented in the cleaning code.

## 14. Database Design

The SQLite database uses two related tables.
Categories
categories
-------------------------
category_id     PRIMARY KEY
category_name   UNIQUE
Books
books
-------------------------
book_id         PRIMARY KEY
title
price_gbp
price_inr
rating
in_stock
category_id     FOREIGN KEY

Relationship:

categories
     |
     | category_id
     |
     ↓
books.category_id

This avoids repeatedly storing the category name for every book and provides a normalized relational structure.

## 15. SQL Queries

The project demonstrates the required SQL operations.
SELECT / WHERE
Example:
SELECT title, price_gbp
FROM books
WHERE price_gbp > 30;
This returns books whose GBP price is greater than 30.

## 16.ORDER BY
SELECT title, rating
FROM books
ORDER BY rating DESC;

This sorts books from highest rating to lowest rating.

## 16.LIMIT
SELECT title, price_gbp
FROM books
ORDER BY price_gbp DESC
LIMIT 10;
This returns the 10 most expensive books.

## 17.DISTINCT
SELECT DISTINCT category_name
FROM categories;
This returns each category only once.

## 18.BETWEEN
SELECT title, price_gbp
FROM books
WHERE price_gbp BETWEEN 10 AND 30;
This returns books whose price is between £10 and £30.

## 19.JOIN
SELECT
    b.title,
    b.rating,
    c.category_name
FROM books b
JOIN categories c
    ON b.category_id = c.category_id;

This combines information from the books and categories tables.

## 20. Pandas Verification
The project also reads SQL query results into pandas using:
pd.read_sql()
The JOIN result is independently reproduced using:
pd.merge()
The two results are compared to verify that the pandas operation produces the same result as the SQL JOIN.