from collections.abc import Iterable

from anyio import to_thread
from dependency_injector.wiring import Provide, inject

from domains.books.entities.events import BookCreatedV1

from ._data_access_interfaces import BookEventGatewayInterface, BookRepositoryInterface
from .dto import Book, BookData
from .entities.models import BookModel


class BookService:
    book_repository: BookRepositoryInterface
    event_gateway: BookEventGatewayInterface

    @inject
    def __init__(
        self,
        book_repository: BookRepositoryInterface = Provide[
            BookRepositoryInterface.__name__
        ],
        event_gateway: BookEventGatewayInterface = Provide[
            BookEventGatewayInterface.__name__
        ],
    ) -> None:
        super().__init__()
        self.book_repository = book_repository
        self.event_gateway = event_gateway

    async def create_book(self, book: BookData) -> Book:
        # Example of CPU intensive task, run in a different thread
        # Using processes could be better, but it would bring technical complexity
        # https://anyio.readthedocs.io/en/3.x/subprocesses.html#running-functions-in-worker-processes
        book_data_altered = await to_thread.run_sync(
            some_cpu_intensive_blocking_task, book.model_dump()
        )
        book_model = BookModel(**book_data_altered)
        book = Book.model_validate(
            await self.book_repository.save(book_model), from_attributes=True
        )
        await self.event_gateway.emit(BookCreatedV1(book_model))
        return book

    async def list_books(self) -> Iterable[Book]:
        books = await self.book_repository.find()
        return [Book.model_validate(x, from_attributes=True) for x in books]


def some_cpu_intensive_blocking_task(book: dict) -> dict:
    # This is just an example placeholder,
    # there's nothing to test.
    return book  # pragma: no cover
