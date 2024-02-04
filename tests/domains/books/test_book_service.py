from unittest.mock import AsyncMock, MagicMock, patch

from domains.books import _service, dto
from domains.books._gateway_interfaces import BookEventGatewayInterface
from domains.books._models import BookModel
from domains.books._tasks import book_cpu_intensive_task


async def test_create_book(book_repository):
    event_gateway = MagicMock(spec=BookEventGatewayInterface)
    book_service = _service.BookService(
        book_repository=book_repository,
        event_gateway=event_gateway,
    )
    book = dto.Book(
        title="test",
        author_name="other",
    )
    mocked_task_return = MagicMock
    mocked_task_return.get = MagicMock(return_value=book_cpu_intensive_task(book))
    with patch.object(
        book_cpu_intensive_task, "delay", return_value=mocked_task_return
    ):
        returned_book = await book_service.create_book(book)
    assert book.title == returned_book.title
    assert book.author_name == returned_book.author_name
    assert returned_book.book_id is not None
    event_gateway.emit.assert_called_once()
    book_repository.save.assert_called_once()


async def test_list_books(book_repository):
    event_gateway = MagicMock(spec=BookEventGatewayInterface)
    book_service = _service.BookService(
        book_repository=book_repository,
        event_gateway=event_gateway,
    )
    book = BookModel(
        book_id=2,
        title="test",
        author_name="other",
    )

    book_repository.find = AsyncMock(return_value=[book])

    returned_books = await book_service.list_books()
    assert [dto.Book.model_validate(book, from_attributes=True)] == returned_books
    book_repository.find.assert_called_once()
