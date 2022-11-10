from dependency_injector.wiring import inject, Provide

from app.domains.books import BookService
from app.domains.books.local.interfaces import BookRepositoryInterface
from app.models import Book


class LocalBookService(BookService):
    book_repository: BookRepositoryInterface

    @inject
    def __init__(
            self,
            book_repository: BookRepositoryInterface = Provide[BookRepositoryInterface.__name__]
    ) -> None:
        super().__init__()
        self.book_repository = book_repository

    def create_book(self, book: Book) -> Book:
        return self.book_repository.create_book(book)
