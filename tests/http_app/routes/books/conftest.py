from unittest.mock import MagicMock

import pytest

from domains.books.boundary_interfaces import BookServiceInterface


@pytest.fixture
def book_service() -> MagicMock:
    svc = MagicMock(autospec=BookServiceInterface)
    svc.create_book = MagicMock(side_effect=lambda x: x)

    return svc
