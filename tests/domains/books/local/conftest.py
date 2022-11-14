from unittest.mock import MagicMock

import pytest

from app.domains.books.local import BookRepositoryInterface


@pytest.fixture
def book_repository() -> MagicMock:
    repo = MagicMock(autospec=BookRepositoryInterface)
    repo.create_book = MagicMock(side_effect=lambda x: x)

    return repo
