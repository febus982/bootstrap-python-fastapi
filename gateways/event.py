from structlog import get_logger

from domains.books.entities.cloudevent_base import BaseEvent


class NullEventGateway:
    async def emit(
        self, event: BaseEvent
    ) -> None:  # pragma: no cover # No need to test this
        logger = get_logger()
        await logger.ainfo(
            "Event emitted",
            attributes=event.get_attributes(),
            data=event.data.model_dump() if event.data else None,
        )
