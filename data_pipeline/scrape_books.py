import requests
from bs4 import BeautifulSoup
import pandas as pd


# ============================================================
# DATA PIPELINE - SCRAPE BOOKS
# ============================================================


BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

books_data = []


# ============================================================
# 1. SCRAPE FIRST 5 PAGES
# ============================================================

for page_number in range(1, 6):

    url = BASE_URL.format(page_number)

    print("=" * 60)
    print("Scraping page:", page_number)
    print("URL:", url)
    print("=" * 60)

    response = requests.get(url)

    print("Status code:", response.status_code)

    # If a page fails, don't crash the entire pipeline.
    if response.status_code != 200:
        print("Could not download this page. Skipping...")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all(
        "article",
        class_="product_pod"
    )

    print("Books found:", len(books))


    # ========================================================
    # 2. EXTRACT BOOK INFORMATION
    # ========================================================

    for book in books:

        try:

            # Book title
            title = book.h3.a["title"]

            # Price
            price = book.find(
                "p",
                class_="price_color"
            ).text.strip()

            # Availability
            availability = book.find(
                "p",
                class_="instock availability"
            ).text.strip()

            # Rating
            rating = book.p["class"][1]

            # ------------------------------------------------
            # CATEGORY
            # ------------------------------------------------
        

            book_url = book.h3.a["href"]

            # Convert relative URL into complete URL
            if not book_url.startswith("http"):
                book_url = (
                    "https://books.toscrape.com/catalogue/"
                    + book_url.replace("../", "")
                )

            book_response = requests.get(book_url)

            if book_response.status_code == 200:

                book_soup = BeautifulSoup(
                    book_response.text,
                    "html.parser"
                )

                breadcrumb = book_soup.find(
                    "ul",
                    class_="breadcrumb"
                )

                if breadcrumb:

                    breadcrumb_items = breadcrumb.find_all("li")

                    # Category is normally the third item
                    if len(breadcrumb_items) >= 3:
                        category = breadcrumb_items[2].get_text(
                            strip=True
                        )
                    else:
                        category = "Unknown"

                else:
                    category = "Unknown"

            else:
                category = "Unknown"


            # ------------------------------------------------
            # SAVE BOOK
            # ------------------------------------------------

            books_data.append({
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
                "category": category
            })


        except Exception as e:

            print("Could not parse book:", e)

            # Skip only the problematic book
            continue


# ============================================================
# 3. CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(books_data)


# ============================================================
# 4. DISPLAY RESULTS
# ============================================================

print()
print("=" * 60)
print("TOTAL BOOKS SCRAPED:", len(df))
print("=" * 60)

print()

print(df.head())


# ============================================================
# 5. DISPLAY CATEGORY COUNT
# ============================================================

print()
print("Books per category:")
print(df["category"].value_counts())


# ============================================================
# 6. SAVE RAW CSV
# ============================================================

df.to_csv(
    "books_raw.csv",
    index=False
)

print()
print("Raw data saved successfully to books_raw.csv")