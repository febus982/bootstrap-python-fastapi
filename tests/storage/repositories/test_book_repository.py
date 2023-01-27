from unittest.mock import MagicMock

import pytest
from sqlalchemy_bind_manager.exceptions import UnsupportedBind

from domains.books._local import BookModel
from storage.repositories.book_repository import BookRepository


async def test_repository_fails_if_no_async_bind_passed():
    mocked_sa_manager = MagicMock()
    mocked_sa_manager.get_bind.return_value = "string_is_not_async_bind"
    with pytest.raises(UnsupportedBind):
        repo = BookRepository(sa_manager=mocked_sa_manager)


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
