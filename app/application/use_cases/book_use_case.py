from app.domain.book import Book


class BookUseCase:
    def __init__(self, repository):
        self._repository = repository

    def add_book(self, book):
        book = Book(**book.dict())
        return self._repository.add(book)
