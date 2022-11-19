from abc import ABC, abstractmethod

from .models import BookModel


class BookRepositoryInterface(ABC):
    @abstractmethod
    def create_book(self, book: BookModel) -> BookModel:
        pass
