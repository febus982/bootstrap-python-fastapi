from app.domains.books._local import BookModel
from app.storage.repositories.book_repository import BookRepository


def test_create_book(testapp):
    repo = BookRepository()
    with repo._sa_manager.get_session() as session:
        book = session.get(BookModel, 1)
        assert book is None

    repo.save(
        BookModel(
            title="pippo",
            author_name="pluto",
            book_id=1,
        )
    )

    with repo._sa_manager.get_session() as session:
        book = session.get(BookModel, 1)
        assert book is not None
        assert book.book_id == 1
