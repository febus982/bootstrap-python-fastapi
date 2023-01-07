from unittest.mock import MagicMock

from domains.books import Book
from domains.books._local import LocalBookService


def test_create_book(book_repository):
    service = LocalBookService(book_repository=book_repository)
    book = Book(
        title="test",
        author_name="other",
    )
    returned_book = service.create_book(book)
    assert book == returned_book
    book_repository.save.assert_called_once()


def test_list_books(book_repository):
    service = LocalBookService(book_repository=book_repository)
    book = Book(
        title="test",
        author_name="other",
    )
    book_repository.find = MagicMock(side_effect=lambda: book)
    returned_books = service.list_books()
    assert [book] == returned_books
    book_repository.find.assert_called_once()
