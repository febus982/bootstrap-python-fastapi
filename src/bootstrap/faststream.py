# from typing import Dict, Union
#
# import structlog
# # from domains.events import get_topic_registry
# from faststream.redis import RedisBroker
# from faststream.redis.publisher.asyncapi import AsyncAPIPublisher
# from opentelemetry.instrumentation.faststream import RedisOtelMiddleware
#
# from .config import AppConfig
#
#
# def init_broker(config: AppConfig) -> RedisBroker:
#     broker = RedisBroker(
#         config.EVENTS.REDIS_BROKER_URL,
#         middlewares=(RedisOtelMiddleware,),
#         logger=structlog.getLogger("faststream.broker"),
#     )
#
#     return broker
#
#
# def init_publishers(
#     broker: RedisBroker,
# ) -> Dict[str, AsyncAPIPublisher]:
#     return {
#         topic: broker.publisher(topic, schema=Union[event_types])
#         for topic, event_types in get_topic_registry().items()
#     }
