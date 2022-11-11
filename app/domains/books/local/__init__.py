from dependency_injector.wiring import inject, Provide

from app.domains.books import BookService, Book
from app.domains.books.local.interfaces import BookRepositoryInterface
from app.domains.books.local.models import BookModel


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
        return Book.from_orm(
            self.book_repository.create_book(BookModel(**book.dict()))
        )
