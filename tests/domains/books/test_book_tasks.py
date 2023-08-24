from unittest.mock import MagicMock, patch

from domains.books.service import BookService
from domains.books.tasks import book_created


@patch.object(BookService, "book_created_event_handler", return_value=None)
def test_book_created_task(mocked_task_handler: MagicMock):
    book_created(123)
    mocked_task_handler.assert_called_once_with(123)
