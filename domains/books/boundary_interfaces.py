from collections.abc import Iterable
from typing import Protocol

from .dto import BookData, Book


class BookServiceInterface(Protocol):
    async def create_book(self, book: BookData) -> Book:
        ...

    async def list_books(self) -> Iterable[Book]:
        ...
