from collections.abc import Iterator
from secrets import randbelow
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from domains.books import BookService, dto
from fastapi import FastAPI
from http_app import create_app


@pytest.fixture
def book_service() -> Iterator[MagicMock]:
    svc = MagicMock(autospec=BookService)
    svc.create_book = AsyncMock(
        side_effect=lambda book: dto.Book(book_id=randbelow(1000), **book.model_dump())
    )
    svc.list_books = AsyncMock(
        return_value=[
            dto.Book(
                book_id=123,
                title="The Shining",
                author_name="Stephen King",
            )
        ]
    )

    with patch("domains.books.BookService.__new__", return_value=svc):
        yield svc


@pytest.fixture(scope="function")
def testapp(test_config, book_service) -> Iterator[FastAPI]:
    # We don't need the storage to test the HTTP app
    with patch("bootstrap.bootstrap.init_storage", return_value=None):
        yield create_app(test_config=test_config)
