from typing import Iterable, Protocol, runtime_checkable

from .dto import Book, BookData


@runtime_checkable
class BookServiceInterface(Protocol):
    async def create_book(self, book: BookData) -> Book:
        ...

    async def list_books(self) -> Iterable[Book]:
        ...

    async def book_created_event_handler(self, book_id: int) -> None:
        ...
