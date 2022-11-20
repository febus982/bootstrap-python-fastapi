from app.domains.books.local import BookModel
from app.storage.repositories.book_repository import BookRepository


def test_create_book(testapp):
    repo = BookRepository()
    with repo.sa_manager.get_session() as session:
        book = session.get(BookModel, 1)
        assert book is None

    repo.create_book(BookModel(
        title="pippo",
        author_name="pluto",
        book_id=1,
    ))

    with repo.sa_manager.get_session() as session:
        book = session.get(BookModel, 1)
        assert book is not None
        assert book.book_id == 1
