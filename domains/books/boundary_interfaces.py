from collections.abc import Iterable
from typing import Protocol

from .dto import BookData, Book


class BookServiceInterface(Protocol):
    def create_book(self, book: BookData) -> Book:
        ...

    def list_books(self) -> Iterable[Book]:
        ...
