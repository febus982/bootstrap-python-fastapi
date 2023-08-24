from asgiref.sync import async_to_sync
from celery import shared_task

from domains.books.service import BookService


@shared_task()
def book_created(book_id):
    book_service = BookService()

    """
    This might not work if we call directly hello() from an app with
    an already running async loop. It would be great having either
    native async support or a better solution to identify running loops.
    For now, we'll assume this is always executed in the worker.
    In order to call this directly we might have to use the opposite
    `sync_to_async` wrapper from asgiref.sync
    """
    return async_to_sync(book_service.book_created_event_handler)(book_id)
