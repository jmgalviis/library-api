from fastapi import HTTPException

from app.domain.book import Book


class BookUseCase:
    def __init__(self, repository):
        self._repository = repository

    def add_book(self, book):
        book = Book(**book.dict())
        try:
            return self._repository.add(book)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_books_by_author_or_year(self, author: str = None, year: int = None):
        return self._repository.get_by_author_or_year(author, year)

    def get_by_id(self, book_id: int):
        book = self._repository.get_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def update(self, book_id: int, updates: dict):
        book = self._repository.get_by_id(book_id)
        return self._repository.update(book, updates)

