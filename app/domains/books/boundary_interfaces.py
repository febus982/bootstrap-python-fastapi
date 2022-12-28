from typing import Protocol

from .dto import BookData, Book


class BookService(Protocol):
    def create_book(self, book: BookData) -> Book:
        ...
