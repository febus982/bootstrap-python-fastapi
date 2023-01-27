from domains.books._local import BookModel
from storage.repositories.book_repository import BookRepository


async def test_create_book():
    repo = BookRepository()
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
