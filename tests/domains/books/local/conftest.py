from unittest.mock import MagicMock

import pytest

from domains.books._local import BookRepositoryInterface


@pytest.fixture
def book_repository() -> MagicMock:
    repo = MagicMock(spec=BookRepositoryInterface)
    repo.save = MagicMock(side_effect=lambda x: x)

    return repo
