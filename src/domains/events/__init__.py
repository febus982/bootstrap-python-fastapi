from typing import Dict

from .books import BookCreatedV1
from .cloudevent_base import BaseEvent


def get_topic_registry() -> Dict[type[BaseEvent], str]:
    # Ideally we can extract this in a reusable package
    # to reuse it in multiple applications
    return {BookCreatedV1: "books_topic"}
