from collections.abc import Iterable

from anyio import to_thread
from dependency_injector.wiring import Provide, inject
from structlog import get_logger

from domains.books.events import BookCreatedV1, BookCreatedV1Data
from domains.books.models import BookModel

from ._data_access_interfaces import BookEventGatewayInterface, BookRepositoryInterface
from .dto import Book, BookData
from .tasks import book_cpu_intensive_task


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
        # Example of CPU intensive task ran in a different thread
        # Using processes could be better, but it would bring technical complexity
        # https://anyio.readthedocs.io/en/3.x/subprocesses.html#running-functions-in-worker-processes
        book_data_altered: dict = await to_thread.run_sync(
            self.some_cpu_intensive_blocking_task, book.model_dump()
        )

        # Example of CPU intensive task ran in a celery task. We should not rely on
        # celery if we need to wait the operation result. The worker could be terminated
        # (e.g. during deployments) and this function would time out or raise an error.
        book_cpu_intensive_task.delay(book)

        book_model = BookModel(**book_data_altered)
        book = Book.model_validate(
            await self.book_repository.save(book_model), from_attributes=True
        )
        await self.event_gateway.emit(
            BookCreatedV1(
                data=BookCreatedV1Data(
                    book_id=book_model.book_id,
                    title=book_model.title,
                    author_name=book_model.author_name,
                )
            )
        )
        return book

    async def list_books(self) -> Iterable[Book]:
        books = await self.book_repository.find()
        return [Book.model_validate(x, from_attributes=True) for x in books]

    async def book_created_event_handler(self, book_id) -> None:  # pragma: no cover
        # This is just an example placeholder, there's nothing to test.
        logger = get_logger()
        await logger.ainfo(f"Processed book crated event for id `{book_id}`")

    def some_cpu_intensive_blocking_task(self, book: dict) -> dict:
        # This is just an example placeholder,
        # there's nothing to test.
        return book  # pragma: no cover
