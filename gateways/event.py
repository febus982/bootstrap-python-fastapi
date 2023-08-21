from structlog import get_logger

from domains.cloudevent_base import BaseEvent


class NullEventGateway:
    async def emit(
        self, event: BaseEvent
    ) -> None:  # pragma: no cover # No need to test this
        logger = get_logger()
        await logger.ainfo(
            "Event emitted",
            cloudevent=event.model_dump(),
        )
