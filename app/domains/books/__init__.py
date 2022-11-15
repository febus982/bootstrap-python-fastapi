from abc import ABC, abstractmethod

from .dto import Book, BookData


class BookService(ABC):
    @abstractmethod
    def create_book(self, book: BookData) -> Book:
        pass
