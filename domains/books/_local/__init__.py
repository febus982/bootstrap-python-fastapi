from collections.abc import Iterable

from dependency_injector.wiring import inject, Provide

from domains.books.dto import Book, BookData

from .data_access_interfaces import BookRepositoryInterface
from .models import BookModel


class LocalBookService:
    book_repository: BookRepositoryInterface

    @inject
    def __init__(
        self,
        book_repository: BookRepositoryInterface = Provide[
            BookRepositoryInterface.__name__
        ],
    ) -> None:
        super().__init__()
        self.book_repository = book_repository

    def create_book(self, book: BookData) -> Book:
        return Book.from_orm(self.book_repository.save(BookModel(**book.dict())))

    def list_books(self) -> Iterable[Book]:
        books = self.book_repository.find()
        return [Book.from_orm(x) for x in books]
