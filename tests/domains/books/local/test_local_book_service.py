from unittest.mock import AsyncMock

from domains.books import Book, BookService
from domains.books._models import BookModel


async def test_create_book(book_repository):
    service = BookService(book_repository=book_repository)
    book = Book(
        title="test",
        author_name="other",
    )
    returned_book = await service.create_book(book)
    assert book == returned_book
    book_repository.save.assert_called_once()


async def test_list_books(book_repository):
    service = BookService(book_repository=book_repository)
    book = BookModel(
        book_id=2,
        title="test",
        author_name="other",
    )

    book_repository.find = AsyncMock(return_value=[book])

    returned_books = await service.list_books()
    assert [Book.model_validate(book, from_attributes=True)] == returned_books
    book_repository.find.assert_called_once()
