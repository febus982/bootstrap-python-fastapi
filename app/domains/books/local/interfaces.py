from abc import ABC, abstractmethod

from app.domains.books.local.models import BookModel


class BookRepositoryInterface(ABC):
    @abstractmethod
    def create_book(self, book: BookModel) -> BookModel:
        ...
