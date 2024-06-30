from typing import Collection, Dict

from .books import BookCreatedV1, BookUpdatedV1
from .cloudevent_base import BaseEvent


def get_topic_registry() -> Dict[str, Collection[type[BaseEvent]]]:
    # Ideally we can extract this in a reusable package
    # to reuse it in multiple applications
    return {
        "books_topic": (BookCreatedV1, BookUpdatedV1),
    }
