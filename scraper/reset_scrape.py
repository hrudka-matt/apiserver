import sys
import os

# Ensure the parent directory (your project root) is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraper.selenium_scraper import BookScraper
from db.sqlite_handler import SQLiteHandler


# 1. Delete the existing DB
if os.path.exists("books.db"):
    os.remove("books.db")
    print("Deleted existing books.db")

# 2. Recreate DB and table
with SQLiteHandler() as db:
    db.create_books_table()
    print("Created fresh books table")

# 3. Scrape and reinsert books
scraper = BookScraper()
books = scraper.scrape_all_books("http://books.toscrape.com/catalogue/category/books_1/index.html")

with SQLiteHandler() as db:
    db.insert_books(books)
    print(f"Inserted {len(books)} books into the database")
