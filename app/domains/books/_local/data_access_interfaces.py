from typing import Protocol

from .models import BookModel


class BookRepositoryInterface(Protocol):
    def save(self, book: BookModel) -> BookModel:
        ...
