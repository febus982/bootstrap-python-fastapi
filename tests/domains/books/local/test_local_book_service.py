from unittest.mock import AsyncMock, MagicMock

from domains.books import dto, service
from domains.books.entities.models import BookModel
from gateways.event import EventGatewayInterface


async def test_create_book(book_repository):
    event_gateway = MagicMock(spec=EventGatewayInterface)
    book_service = service.BookService(
        book_repository=book_repository,
        event_gateway=event_gateway,
    )
    book = dto.Book(
        title="test",
        author_name="other",
    )
    returned_book = await book_service.create_book(book)
    assert book == returned_book
    event_gateway.emit.assert_called_once()
    book_repository.save.assert_called_once()


async def test_list_books(book_repository):
    event_gateway = MagicMock(spec=EventGatewayInterface)
    book_service = service.BookService(
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
    assert [dto.Book.from_orm(book)] == returned_books
    book_repository.find.assert_called_once()
