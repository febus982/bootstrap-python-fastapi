from unittest.mock import MagicMock

import pytest

from app.domains.books import BookService


@pytest.fixture
def book_service() -> MagicMock:
    repo = MagicMock(autospec=BookService)
    repo.create_book = MagicMock(side_effect=lambda x: x)

    return repo
