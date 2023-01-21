from unittest.mock import MagicMock

from domains.books.dto import Book
from domains.books._local import LocalBookService, BookModel


async def test_create_book(book_repository):
    service = LocalBookService(book_repository=book_repository)
    book = Book(
        title="test",
        author_name="other",
    )
    returned_book = await service.create_book(book)
    assert book == returned_book
    book_repository.save.assert_called_once()


async def test_list_books(book_repository):
    service = LocalBookService(book_repository=book_repository)
    book = BookModel(
        book_id=2,
        title="test",
        author_name="other",
    )
    book_repository.find = MagicMock(side_effect=lambda: [book])
    returned_books = await service.list_books()
    assert [Book.from_orm(book)] == returned_books
    book_repository.find.assert_called_once()
