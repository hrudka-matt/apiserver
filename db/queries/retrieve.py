# backend/db/queries/retrieve.py

import sqlite3

def preview_books(limit=5):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books LIMIT ?", (limit,))
    results = cursor.fetchall()
    conn.close()

    for row in results:
        print(row)
