from unittest.mock import AsyncMock, MagicMock

from domains.books import Book, BookService
from entities.models import BookModel
from gateways.event import EventGatewayInterface


async def test_create_book(book_repository):
    event_gateway = MagicMock(spec=EventGatewayInterface)
    service = BookService(
        book_repository=book_repository,
        event_gateway=event_gateway,
    )
    book = Book(
        title="test",
        author_name="other",
    )
    returned_book = await service.create_book(book)
    assert book == returned_book
    event_gateway.emit.assert_called_once()
    book_repository.save.assert_called_once()


async def test_list_books(book_repository):
    event_gateway = MagicMock(spec=EventGatewayInterface)
    service = BookService(
        book_repository=book_repository,
        event_gateway=event_gateway,
    )
    book = BookModel(
        book_id=2,
        title="test",
        author_name="other",
    )

    book_repository.find = AsyncMock(return_value=[book])

    returned_books = await service.list_books()
    assert [Book.from_orm(book)] == returned_books
    book_repository.find.assert_called_once()
