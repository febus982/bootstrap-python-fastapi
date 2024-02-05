"""
Tasks defined in this module are considered intensive operations
that happen as part of one of the BookService methods,
therefore we shouldn't invoke again the book service directly
from here.

Tasks that invoke the BookService could exist (e.g. an event
worker), there are 2 options to implement them:
- Create a different module, that would behave similar to HTTP
routes, and invoke the service from there.
- Invoke the service using inversion of control.

IMPORTANT: It's dangerous to have nested task when they depend
on each other's result. If you find yourself in this scenario
it is probably better to redesign your application. If this is
not possible, then celery provides task synchronisation primitives.

https://docs.celeryq.dev/en/stable/userguide/tasks.html#avoid-launching-synchronous-subtasks
"""

import logging

from celery import shared_task


@shared_task()
def book_cpu_intensive_task(book_id: str, **kwargs) -> str:
    logging.info("Book CPU intensive executed", extra={"book_id": book_id})
    return book_id
