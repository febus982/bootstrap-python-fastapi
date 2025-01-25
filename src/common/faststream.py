# from typing import Dict, Union
from typing import Optional

import structlog
from faststream import Logger

# from domains.events import get_topic_registry
from faststream.redis import RedisRouter, RedisBroker, fastapi

# from faststream.redis.publisher.asyncapi import AsyncAPIPublisher
from opentelemetry.instrumentation.faststream import RedisOtelMiddleware

from common.config import EventConfig
from domains import event_registry
from event_consumer import register_subscribers

logger = structlog.getLogger(__name__)


def init_router(config: EventConfig) -> RedisRouter:
    broker = RedisBroker(
        config.REDIS_BROKER_URL,
        middlewares=(RedisOtelMiddleware,),
        logger=structlog.getLogger("faststream.broker"),
    )

    router = RedisRouter()
    register_publishers(router, config.TOPIC)
    if config.IS_SUBSCRIBER:
        register_subscribers(router, config.TOPIC)

    broker.include_router(router)
    return router




def register_publishers(router: RedisRouter, topic: Optional[str] = None):
    if topic is not None and topic in event_registry.keys():
        topics_map = {topic: event_registry[topic]}
    else:
        topics_map = event_registry.copy()

    for topic, event_type in topics_map.items():
        router.publisher(topic, schema=event_registry[topic])
