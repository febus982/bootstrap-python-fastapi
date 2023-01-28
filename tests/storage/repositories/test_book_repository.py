from domains.books._local import BookModel
from storage.repositories.book_repository import BookRepository


async def test_create_book(test_sa_manager):
    """
    We are testing the concrete class, therefore we get only the bind
    using the DI container
    """
    repo = BookRepository(bind=test_sa_manager.get_bind())
    async with repo._UOW.get_session() as session:
        book = await session.get(BookModel, 1)
        assert book is None

    await repo.save(
        BookModel(
            title="pippo",
            author_name="pluto",
            book_id=1,
        )
    )

    async with repo._UOW.get_session() as session:
        book = await session.get(BookModel, 1)
        assert book is not None
        assert book.book_id == 1
