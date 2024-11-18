from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.application.use_cases.book_use_case import BookUseCase
from app.domain.book import Book
from app.domain.schemas import BookCreate, BookResponse
from app.infrastructure.database import get_db
from app.infrastructure.repositories.pg_repositories.pg_book_repository import PGBookRepository

book_router = APIRouter()


@book_router.post("/books/")
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.add(book)


@book_router.get("/book/")
def list_books(author: str = None, year: int = None, db: Session = Depends(get_db)):
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.get_by_author_or_year(author=author, year=year)


@book_router.get("/books/search/", response_model=list[BookResponse])
def search_books(query: str = Query(...), db: Session = Depends(get_db)):
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.search(query=query)


@book_router.get("/books/")
def list_books(db: Session = Depends(get_db)):
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.get_all()


@book_router.get("/books/{book_id}/")
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.get_by_id(book_id=book_id)


@book_router.put("/books/{book_id}/")
def update_book(book_id: int, updates: dict, db: Session = Depends(get_db)):
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.update(book_id=book_id, updates=updates)


@book_router.delete("/books/{book_id}/")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_use_case = BookUseCase(repository=PGBookRepository(db=db))
    return book_use_case.delete(book_id=book_id)
