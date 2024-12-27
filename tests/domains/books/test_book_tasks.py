from unittest.mock import MagicMock, patch

from domains.books._service import BookService
from domains.books._tasks import book_cpu_intensive_task


@patch.object(BookService, "book_created_event_handler", return_value=None)
def test_book_created_task(mocked_task_handler: MagicMock):
    assert book_cpu_intensive_task("some_string") == "some_string"
