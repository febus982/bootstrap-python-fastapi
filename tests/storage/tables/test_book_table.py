from domains.books._models import BookModel
from sqlalchemy_bind_manager._repository import SQLAlchemyAsyncRepository


# This test is to ensure the book table is initialised correctly
async def test_book_table_works(test_sa_manager):
    repo = SQLAlchemyAsyncRepository(
        bind=test_sa_manager.get_bind(), model_class=BookModel
    )
    async with repo._get_session() as session:
        book = await session.get(BookModel, 1)
        assert book is None

    await repo.save(
        BookModel(
            title="pippo",
            author_name="pluto",
            book_id=1,
        )
    )

    async with repo._get_session() as session:
        book = await session.get(BookModel, 1)
        assert book is not None
        assert book.book_id == 1
