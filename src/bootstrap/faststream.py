from contextlib import asynccontextmanager
from typing import Any, Dict, Union

from domains.events import BaseEvent, get_topic_registry
from fastapi import FastAPI
from faststream.broker.core.usecase import BrokerUsecase
from faststream.broker.publisher.proto import PublisherProto
from faststream.redis import RedisBroker
from faststream.types import Lifespan

from .config import AppConfig


def init_broker(config: AppConfig) -> BrokerUsecase[Any, Any]:
    broker = RedisBroker(config.EVENTS.REDIS_BROKER_URL)

    return broker


def init_publishers(
    broker: BrokerUsecase[Any, Any],
) -> Dict[str, PublisherProto[type[BaseEvent]]]:
    return {
        topic: broker.publisher(topic, schema=Union[event_types])
        for topic, event_types in get_topic_registry().items()
    }


def fastapi_lifespan(broker) -> Lifespan:
    @asynccontextmanager
    async def f(app: FastAPI):
        await broker.start()
        try:
            yield
        finally:
            await broker.close()

    return f
