from collections.abc import Iterable

from anyio import to_thread
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
        # Example of CPU intensive task, run in a different thread
        # Using processes could be better, but it would bring technical complexity
        # https://anyio.readthedocs.io/en/3.x/subprocesses.html#running-functions-in-worker-processes
        book_data_altered = await to_thread.run_sync(
            some_cpu_intensive_blocking_task, book.dict()
        )
        book_model = BookModel(**book_data_altered)
        return Book.from_orm(await self.book_repository.save(book_model))

    async def list_books(self) -> Iterable[Book]:
        books = await self.book_repository.find()
        return [Book.from_orm(x) for x in books]


def some_cpu_intensive_blocking_task(book: dict) -> dict:
    # This is just an example placeholder,
    # there's nothing to test.
    return book  # pragma: no cover
