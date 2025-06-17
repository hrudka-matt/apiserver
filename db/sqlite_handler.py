import os
import sqlite3
from typing import List, Optional, Generator
from models.book import Book


class SQLiteHandler:
    def __init__(self, db_path: str = None):
        # this entire method is your constructor
        env_path = os.getenv("BOOKS_DB_PATH")

        if db_path:
            resolved = db_path
        elif env_path:
            resolved = env_path
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            resolved = os.path.join(base_dir, "books.db")

        # ✅ Normalize to an absolute path
        self.db_path = os.path.abspath(resolved)

        self.conn = None
        self.cursor = None
        print(f"📘 SQLite DB Path: {self.db_path}")  # <-- You can add more debug here



    def __enter__(self):
        import threading
        print(f"🔧 Opening SQLite DB on thread {threading.get_ident()}")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def create_books_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price TEXT NOT NULL
            )
        """)

    def insert_book(self, book: Book) -> int:
        self.cursor.execute(
            "INSERT INTO books (title, price) VALUES (?, ?)",
            (book.title, book.price)
        )
        return self.cursor.lastrowid

    def insert_books(self, books: List[Book]):
        self.cursor.executemany(
            "INSERT INTO books (title, price) VALUES (?, ?)",
            [(b.title, b.price) for b in books]
        )

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        self.cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = self.cursor.fetchone()
        if row:
            return Book(id=row[0], title=row[1], price=row[2])
        return None

    def get_all_books(self, limit: int = 100) -> List[Book]:
        self.cursor.execute("SELECT * FROM books LIMIT ?", (limit,))
        return [Book(id=row[0], title=row[1], price=row[2]) for row in self.cursor.fetchall()]

    def update_book(self, book: Book) -> bool:
        self.cursor.execute(
            "UPDATE books SET title = ?, price = ? WHERE id = ?",
            (book.title, book.price, book.id)
        )
        return self.cursor.rowcount > 0

    def delete_book(self, book_id: int) -> bool:
        self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        return self.cursor.rowcount > 0


def get_db_handler() -> Generator[SQLiteHandler, None, None]:
    with SQLiteHandler() as db:
        yield db