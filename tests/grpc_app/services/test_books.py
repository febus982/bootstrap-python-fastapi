from unittest.mock import AsyncMock, MagicMock, patch

from domains.books import dto
from grpc_app import BooksServicer
from grpc_app.generated.books_pb2 import ListBooksRequest, ListBooksResponse


async def test_grpc_server():
    book_service = AsyncMock()
    book_service.list_books.return_value = [
        dto.Book(
            book_id=123,
            title="Some book",
            author_name="Some author",
        )
    ]

    with patch("domains.books.service.BookService.__new__", return_value=book_service):
        servicer = BooksServicer()
        response = await servicer.ListBooks(
            request=ListBooksRequest(),
            context=MagicMock(),
        )

    assert isinstance(response, ListBooksResponse)
    # TODO: Find a better way to test GRPC output
    assert (
        response.SerializeToString().decode()
        == "\n\x1a\x08{\x12\tSome book\x1a\x0bSome author"
    )
