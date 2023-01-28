from collections.abc import Iterator
from random import randint
from unittest.mock import MagicMock, AsyncMock, patch

import pytest
from dependency_injector.providers import Object
from fastapi import FastAPI

from di_container import Container
from domains.books.boundary_interfaces import BookServiceInterface
from domains.books.dto import Book
from http_app import create_app


@pytest.fixture
def book_service() -> MagicMock:
    svc = MagicMock(autospec=BookServiceInterface)
    svc.create_book = AsyncMock(
        side_effect=lambda book: Book(book_id=randint(1, 1000), **book.dict())
    )

    return svc


@pytest.fixture(scope="function")
def testapp(test_config, book_service) -> Iterator[FastAPI]:
    # We don't need the storage to test the HTTP app
    with patch("http_app.init_storage", return_value=None):
        c = Container(config=Object(test_config))
        c.wire(packages=["http_app"])
        with c.BookServiceInterface.override(book_service):
            # yield c
            app = create_app(test_config=test_config)
            yield app
