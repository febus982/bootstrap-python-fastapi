from typing import Collection, Dict, Optional

from .books import BookCreatedV1, BookUpdatedV1
from .cloudevent_base import BaseEvent


def get_topic_registry(
    topic_filter: Optional[Collection[str]] = None,
) -> Dict[str, Collection[type[BaseEvent]]]:
    # Ideally we can extract this in a reusable package
    # to reuse it in multiple applications
    registry: Dict[str, Collection[type[BaseEvent]]] = {
        "books_topic": (BookCreatedV1, BookUpdatedV1),
    }
    if topic_filter:
        return {k: v for k, v in registry.items() if k in topic_filter}
    else:
        return registry
