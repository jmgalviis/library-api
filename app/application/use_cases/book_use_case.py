from app.domain.book import Book


class BookUseCase:
    def __init__(self, repository):
        self._repository = repository

    def add_book(self, book):
        book = Book(**book.dict())
        return self._repository.add(book)

    def get_books_by_author_or_year(self, author: str = None, year: int = None):
        return self._repository.get_by_author_or_year(author, year)
