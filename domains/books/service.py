from collections.abc import Iterable

from anyio import to_thread
from celery.result import AsyncResult
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
        # Example of CPU intensive task, run in a celery task
        book_task: AsyncResult = book_cpu_intensive_task.delay(book)
        # task.get() would block the application, we run it in a thread to remain async
        # we can also build a wrapper coroutine to do this using `asyncio.sleep`
        # and poll the AsyncResult class in case we do not want to use threads
        book_data_altered: BookData = await to_thread.run_sync(book_task.get)
        book_model = BookModel(**book_data_altered.model_dump())
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
