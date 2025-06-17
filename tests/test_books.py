import sqlite3

from fastapi.testclient import TestClient
from main import app
from db.sqlite_handler import SQLiteHandler,get_db_handler

class TestDBHandler(SQLiteHandler):
    def __init__(self):
        super().__init__(db_path=":memory:")
        self.conn = sqlite3.connect(self.db_path,check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_books_table()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

# Override FastAPI dependency
test_db_handler = TestDBHandler()

def override_get_db_handler():
    yield test_db_handler

app.dependency_overrides[get_db_handler] = override_get_db_handler
client = TestClient(app)

def test_crud_book_flow():
    new_book = {"title": "Unit Testing for Humans", "price": "£14.99"}
    response = client.post("/books", json=new_book)
    assert response.status_code == 201, f"POST failed: {response.text}"
    created = response.json()
    book_id = created["id"]

    response = client.get("/books")
    assert response.status_code == 200
    books = response.json()
    assert any(b["id"] == book_id for b in books), f"Book ID {book_id} not found in GET /books"

    updated_data = {"title": "Unit Testing for Professionals", "price": "£18.99"}
    response = client.put(f"/books/{book_id}", json=updated_data)
    assert response.status_code == 200

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204

    response = client.get("/books")
    assert all(b["id"] != book_id for b in response.json()), f"Book ID {book_id} still exists after deletion"
