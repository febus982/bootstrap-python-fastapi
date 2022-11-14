from app.domains.books import Book
from app.domains.books.local import LocalBookService


def test_create_book(book_repository):
    service = LocalBookService(book_repository=book_repository)
    book = Book(
        title="test",
        author_name="other",
    )
    returned_book = service.create_book(book)
    assert book == returned_book
    book_repository.create_book.assert_called_once()
