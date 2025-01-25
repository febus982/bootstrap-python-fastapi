# from typing import Dict, Union
from typing import Optional

import structlog
from faststream.redis import RedisBroker, RedisRouter
from opentelemetry.instrumentation.faststream import RedisOtelMiddleware

from domains import event_registry

from .config import EventConfig

logger = structlog.getLogger(__name__)


def init_broker(config: EventConfig) -> RedisBroker:
    broker = RedisBroker(
        config.REDIS_BROKER_URL,
        middlewares=(RedisOtelMiddleware,),
        logger=structlog.getLogger("faststream.broker"),
    )

    if config.REGISTER_PUBLISHERS:
        router = RedisRouter()
        register_publishers(router, config.SUBSCRIBER_TOPIC)
        broker.include_router(router)

    return broker


def register_publishers(router: RedisRouter, topic: Optional[str] = None):
    if topic is not None and topic in event_registry.keys():
        topics_map = {topic: event_registry[topic]}
    else:
        topics_map = event_registry.copy()

    for topic, event_type in topics_map.items():
        router.publisher(topic, schema=event_registry[topic])
