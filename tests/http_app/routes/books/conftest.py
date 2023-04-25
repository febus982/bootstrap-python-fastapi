from collections.abc import Iterator
from random import randint
from unittest.mock import MagicMock, AsyncMock, patch

import pytest
from fastapi import FastAPI

from domains.books import BookService, Book
from http_app import create_app


@pytest.fixture
def book_service() -> MagicMock:
    svc = MagicMock(autospec=BookService)
    svc.create_book = AsyncMock(
        side_effect=lambda book: Book(book_id=randint(1, 1000), **book.dict())
    )

    with patch("domains.books._service.BookService.__new__", return_value=svc):
        yield svc


@pytest.fixture(scope="function")
def testapp(test_config, book_service) -> Iterator[FastAPI]:
    # We don't need the storage to test the HTTP app
    with patch("http_app.init_storage", return_value=None):
        yield create_app(test_config=test_config)
