from unittest.mock import MagicMock, AsyncMock

from domains.books.boundary_interfaces import BookServiceInterface
from domains.books.dto import Book
from grpc_app import BooksServicer
from grpc_app.generated.books_pb2 import ListBooksRequest, ListBooksResponse


async def test_grpc_server():
    servicer = BooksServicer()

    book_service = AsyncMock(autospec=BookServiceInterface)
    book_service.list_books.return_value = [
        Book(
            book_id=123,
            title="Some book",
            author_name="Some author",
        )
    ]

    response = await servicer.ListBooks(
        request=ListBooksRequest(),
        context=MagicMock(),
        book_service=book_service,
    )
    assert isinstance(response, ListBooksResponse)
    # TODO: Find a better way to test GRPC output
    assert (
        response.SerializeToString().decode()
        == "\n\x1a\x08{\x12\tSome book\x1a\x0bSome author"
    )
