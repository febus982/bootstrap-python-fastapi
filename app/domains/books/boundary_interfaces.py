from abc import ABC, abstractmethod

from .dto import BookData, Book


class BookService(ABC):
    @abstractmethod
    def create_book(self, book: BookData) -> Book:
        pass
