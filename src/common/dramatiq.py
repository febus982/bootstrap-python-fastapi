from dramatiq import set_broker, set_encoder
from dramatiq.brokers.stub import StubBroker
from dramatiq.brokers.redis import RedisBroker
from dramatiq.encoder import Encoder, DecodeError, MessageData
from dramatiq.middleware import AsyncIO
from opentelemetry_instrumentor_dramatiq import DramatiqInstrumentor
import orjson
from .config import AppConfig


class ORJSONEncoder(Encoder):
    """Encodes messages as JSON. orjson is much faster than json.
    """

    def encode(self, data: MessageData) -> bytes:
        return orjson.dumps(data)

    def decode(self, data: bytes) -> MessageData:
        try:
            return orjson.loads(data)
        except orjson.JSONDecodeError as e:
            raise DecodeError("failed to decode message %r" % (data,), data, e) from None


def init_dramatiq(config: AppConfig):
    DramatiqInstrumentor().instrument()
    if config.ENVIRONMENT == "test":
        broker = StubBroker()
        # broker.emit_after("process_boot")
    elif config.DRAMATIQ.REDIS_URL is not None:
        broker = RedisBroker(url=config.DRAMATIQ.REDIS_URL)
    else:
        raise RuntimeError("Running a non-test environment without Redis URL set")
    broker.add_middleware(AsyncIO())
    set_broker(broker)
    set_encoder(ORJSONEncoder())
