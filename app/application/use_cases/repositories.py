from abc import ABCMeta, abstractmethod
from typing import List

from app.domain.book import Book


class BookRepository(metaclass=ABCMeta):
    @abstractmethod
    def add(self, book: Book) -> Book:
        pass

    @abstractmethod
    def get_by_id(self, book_id: int) -> Book:
        pass

    @abstractmethod
    def get_by_author_or_year(self, author: str, year: int) -> Book:
        pass

    @abstractmethod
    def search(self, query: str) -> Book:
        pass

    @abstractmethod
    def update(self, book: Book, updates: dict) -> Book:
        pass

    @abstractmethod
    def delete(self, book: Book) -> Book:
        pass

    @abstractmethod
    def get_all(self) -> List[Book]:
        pass

