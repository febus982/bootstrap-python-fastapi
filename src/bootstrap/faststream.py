from typing import Any, Dict, Union

import structlog

from domains.events import BaseEvent, get_topic_registry
from faststream.broker.core.usecase import BrokerUsecase
from faststream.broker.publisher.proto import PublisherProto
from faststream.redis import RedisBroker
from opentelemetry.instrumentation.faststream import RedisOtelMiddleware

from .config import AppConfig


def init_broker(config: AppConfig) -> BrokerUsecase[Any, Any]:
    broker = RedisBroker(
        config.EVENTS.REDIS_BROKER_URL,
        middlewares=(RedisOtelMiddleware,),
        logger=structlog.getLogger("event_broker")
    )

    return broker


def init_publishers(
    broker: BrokerUsecase[Any, Any],
) -> Dict[str, PublisherProto[type[BaseEvent]]]:
    return {
        topic: broker.publisher(topic, schema=Union[event_types])
        for topic, event_types in get_topic_registry().items()
    }
