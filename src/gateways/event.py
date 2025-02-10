import logging

from cloudevents_pydantic.events import CloudEvent


class NullEventGateway:
    async def emit(self, event: CloudEvent) -> None:  # pragma: no cover # No need to test this
        logging.info("Event emitted", extra={"cloudevent": event.model_dump()})
