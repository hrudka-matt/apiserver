from typing import List
from fastapi import APIRouter, Depends, HTTPException
from db.sqlite_handler import SQLiteHandler, get_db_handler
from models.book import Book, BookRequest, BookResponse
from auth.auth_handler import get_current_user
from fastapi import Depends

router = APIRouter()


@router.get("/books", response_model=List[BookResponse])
def get_books(
    db: SQLiteHandler = Depends(get_db_handler),
    user: str = Depends(get_current_user)
):
    try:
        print(f"Authenticated user: {user}")
        books = db.get_all_books()
        print(f"Books retrieved: {books}")
        return books
    except Exception as e:
        print("Error in /books:", e)


@router.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: BookRequest, db: SQLiteHandler = Depends(get_db_handler),current_user: str = Depends(get_current_user)):
    book_id = db.insert_book(Book(title=book.title, price=book.price))
    return Book(id=book_id, title=book.title, price=book.price)

@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated: BookRequest, db: SQLiteHandler = Depends(get_db_handler),current_user: str = Depends(get_current_user)):
    existing = db.get_book_by_id(book_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Book not found")
    existing.title = updated.title
    existing.price = updated.price
    db.update_book(existing)
    return existing

@router.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: SQLiteHandler = Depends(get_db_handler),current_user: str = Depends(get_current_user)):
    if not db.delete_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
