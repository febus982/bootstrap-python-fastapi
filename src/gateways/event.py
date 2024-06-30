from typing import Any, Collection, Dict, Optional, Union

from domains.events import get_topic_registry
from domains.events.cloudevent_base import BaseEvent
from faststream.broker.core.usecase import BrokerUsecase
from faststream.broker.publisher.proto import PublisherProto
from structlog import get_logger


class NullEventGateway:
    async def emit(
        self, event: BaseEvent
    ) -> None:  # pragma: no cover # No need to test this
        logger = get_logger()
        await logger.ainfo(
            "Event emitted",
            cloudevent=event.model_dump(),
        )


class FastStreamGateway:
    _broker: BrokerUsecase[Any, Any]
    _publishers: Dict[type[BaseEvent], PublisherProto[type[BaseEvent]]]

    def __init__(
        self,
        broker: BrokerUsecase[Any, Any],
        topic_filter: Optional[Collection[str]] = None,
    ):
        self._broker = broker
        publishers = {
            topic: broker.publisher(topic, schema=Union[event_types])
            for topic, event_types in get_topic_registry(topic_filter).items()
        }
        self._publishers = {
            event_type: publishers[topic]
            for topic, event_types in get_topic_registry(topic_filter).items()
            for event_type in event_types
        }

    async def emit(
        self, event: BaseEvent
    ) -> None:  # pragma: no cover # No need to test this
        try:
            await self._publishers[type(event)].publish(event)
        except KeyError:
            raise RuntimeError(f"Unknown event type: {type(event)}")
