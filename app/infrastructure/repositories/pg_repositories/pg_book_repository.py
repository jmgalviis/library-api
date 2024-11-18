from app.application.use_cases.repositories import BookRepository
from app.domain.book import Book


class PGBookRepository(BookRepository):
    def __init__(self, db):
        self._db = db

    def add(self, book: Book) -> Book:
        self._db.add(book)
        self._db.commit()
        self._db.refresh(book)
        return book

    def get_by_id(self, book_id: int) -> Book:
        pass

    def get_by_author_or_year(self, author: str, year: int) -> Book:
        query = self._db.query(Book)
        if author:
            query = query.filter(Book.author == author)
        if year:
            query = query.filter(Book.year == year)
        return query.all()

    def search(self, query: str) -> Book:
        pass

    def update(self, book_id: int) -> Book:
        pass

    def delete(self, book_id: int) -> Book:
        pass
