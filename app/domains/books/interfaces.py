from abc import ABC, abstractmethod

from app.models import Book


class BookRepositoryInterface(ABC):
    @abstractmethod
    def create_book(self, book: Book) -> Book:
        ...
