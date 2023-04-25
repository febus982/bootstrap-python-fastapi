from collections.abc import Iterable

from dependency_injector.wiring import Provide, inject

from ._data_access_interfaces import BookRepositoryInterface
from ._dto import Book, BookData
from ._models import BookModel


class BookService:
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

    async def create_book(self, book: BookData) -> Book:
        return Book.from_orm(await self.book_repository.save(BookModel(**book.dict())))

    async def list_books(self) -> Iterable[Book]:
        books = await self.book_repository.find()
        return [Book.from_orm(x) for x in books]
