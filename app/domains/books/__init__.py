from abc import ABC, abstractmethod

from .dto import Book


class BookService(ABC):
    @abstractmethod
    def create_book(self, book: Book) -> Book:
        pass
