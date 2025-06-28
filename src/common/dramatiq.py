import logging

import orjson
from dramatiq import set_broker, set_encoder
from dramatiq.broker import Broker
from dramatiq.brokers.redis import RedisBroker
from dramatiq.brokers.stub import StubBroker
from dramatiq.encoder import DecodeError, Encoder, MessageData
from dramatiq.middleware import AsyncIO

from .config import AppConfig


class ORJSONEncoder(Encoder):
    """Encodes messages as JSON. orjson is much faster than json."""

    def encode(self, data: MessageData) -> bytes:
        return orjson.dumps(data)

    def decode(self, data: bytes) -> MessageData:
        try:
            return orjson.loads(data)
        except orjson.JSONDecodeError as e:
            raise DecodeError("failed to decode message %r" % (data,), data, e) from None


def init_dramatiq(config: AppConfig):
    broker: Broker

    if config.DRAMATIQ.REDIS_URL is not None:
        broker = RedisBroker(url=config.DRAMATIQ.REDIS_URL)
    else:
        broker = StubBroker()
        # broker.emit_after("process_boot")
        if config.ENVIRONMENT not in ["test", "local"]:
            logging.critical(
                "Running a non-test/non-local environment without Redis URL set",
                extra={"ENVIRONMENT": config.ENVIRONMENT},
            )
    broker.add_middleware(AsyncIO())
    set_broker(broker)
    set_encoder(ORJSONEncoder())
