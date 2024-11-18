from typing import List

from sqlalchemy import or_, cast, String

from app.application.use_cases.repositories import BookRepository
from app.domain.book import Book


class PGBookRepository(BookRepository):
    def __init__(self, db):
        self._db = db

    def add(self, book: Book) -> Book:
        existing_book = self._db.query(Book).filter(Book.isbn == book.isbn).first()
        if existing_book:
            raise ValueError(f"A book with ISBN {book.isbn} already exists.")
        self._db.add(book)
        self._db.commit()
        self._db.refresh(book)
        return book

    def get_by_id(self, book_id: int) -> Book:
        return self._db.query(Book).filter(Book.id == book_id).first()

    def get_by_author_or_year(self, author: str, year: int) -> Book:
        query = self._db.query(Book)
        if author:
            query = query.filter(Book.author == author)
        if year:
            query = query.filter(Book.year == year)
        return query.all()

    def search(self, query: str) -> Book:
        results = self._db.query(Book).filter(
            or_(
                Book.title.ilike(f"%{query}%"),
                Book.author.ilike(f"%{query}%"),
                cast(Book.year, String).ilike(f"%{query}%"),
                Book.isbn.ilike(f"%{query}%")
            )
        ).all()
        return results

    def update(self, book: Book, updates: dict) -> Book:
        if book:
            for key, value in updates.items():
                setattr(book, key, value)
            self._db.commit()
            self._db.refresh(book)
        return book

    def delete(self, book: Book) -> Book:
        try:
            self._db.delete(book)
            self._db.commit()
        except Exception as e:
            raise ValueError(f"Error deleting book: {e}")

    def get_all(self) -> List[Book]:
        return self._db.query(Book).all()
