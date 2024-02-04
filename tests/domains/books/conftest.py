from unittest.mock import AsyncMock, MagicMock

import pytest
from domains.books._gateway_interfaces import BookRepositoryInterface


@pytest.fixture
def book_repository() -> MagicMock:
    def _save_book(x):
        x.book_id = 123
        return x

    repo = MagicMock(spec=BookRepositoryInterface)
    repo.save = AsyncMock(side_effect=_save_book)

    return repo
