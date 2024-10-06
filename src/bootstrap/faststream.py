# from typing import Dict, Union
from typing import Optional

import structlog
from faststream import Logger

# from domains.events import get_topic_registry
from faststream.redis import RedisBroker

# from faststream.redis.publisher.asyncapi import AsyncAPIPublisher
from opentelemetry.instrumentation.faststream import RedisOtelMiddleware

from domains import event_registry

from .config import AppConfig


def init_broker(config: AppConfig) -> RedisBroker:
    broker = RedisBroker(
        config.EVENTS.REDIS_BROKER_URL,
        middlewares=(RedisOtelMiddleware,),
        logger=structlog.getLogger("faststream.broker"),
    )
    register_publishers(broker, config.EVENTS.TOPIC)
    register_subscribers(broker, config.EVENTS.TOPIC)

    return broker


def register_subscribers(broker, topic: Optional[str] = None):
    if topic is not None and topic in event_registry.keys():
        topics_map = {topic: event_registry[topic]}
    else:
        topics_map = event_registry.copy()

    for topic, event_type in topics_map.items():

        @broker.subscriber(topic)
        async def handler(msg: event_type, logger: Logger) -> None:  # type: ignore[valid-type]
            logger.info(f"Received message {type(msg)} {msg}")


def register_publishers(broker, topic: Optional[str] = None):
    if topic is not None and topic in event_registry.keys():
        topics_map = {topic: event_registry[topic]}
    else:
        topics_map = event_registry.copy()

    for topic, event_type in topics_map.items():
        broker.publisher(topic, schema=event_registry[topic])


# def init_publishers(
#     broker: RedisBroker,
# ) -> Dict[str, AsyncAPIPublisher]:
#     return {
#         topic: broker.publisher(topic, schema=Union[event_types])
#         for topic, event_types in get_topic_registry().items()
#     }
