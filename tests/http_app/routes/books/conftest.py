from collections.abc import Iterator
from random import randint
from unittest.mock import MagicMock, AsyncMock

import pytest
from dependency_injector.providers import Object

from di_container import Container
from domains.books.boundary_interfaces import BookServiceInterface
from domains.books.dto import Book


@pytest.fixture
def book_service() -> MagicMock:
    svc = MagicMock(autospec=BookServiceInterface)
    svc.create_book = AsyncMock(
        side_effect=lambda book: Book(book_id=randint(1, 1000), **book.dict())
    )

    return svc


@pytest.fixture(scope="function")
def test_container(test_config, book_service) -> Iterator[Container]:
    c = Container(config=Object(test_config))
    with c.BookServiceInterface.override(book_service):
        yield c
