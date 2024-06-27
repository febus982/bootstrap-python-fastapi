from typing import Any

from faststream.broker.core.usecase import BrokerUsecase
from faststream.confluent import KafkaBroker

from .config import AppConfig


def init_broker(config: AppConfig) -> BrokerUsecase[Any, Any]:
    broker = KafkaBroker("localhost:9092")

    return broker
