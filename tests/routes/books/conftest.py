from unittest.mock import MagicMock

import pytest

from app.domains.books import BookServiceInterface


@pytest.fixture
def book_service() -> MagicMock:
    svc = MagicMock(autospec=BookServiceInterface)
    svc.create_book = MagicMock(side_effect=lambda x: x)

    return svc
