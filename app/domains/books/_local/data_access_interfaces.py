from abc import ABC, abstractmethod

from .models import BookModel


class BookRepositoryInterface(ABC):
    @abstractmethod
    def save(self, book: BookModel) -> BookModel:
        pass
