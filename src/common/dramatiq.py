from dramatiq import set_broker
from dramatiq.brokers.stub import StubBroker
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware import AsyncIO
from opentelemetry_instrumentor_dramatiq import DramatiqInstrumentor

from .config import AppConfig


def init_dramatiq(config: AppConfig):
    DramatiqInstrumentor().instrument()
    if config.ENVIRONMENT == "test":
        broker = StubBroker()
        # broker.emit_after("process_boot")
    elif config.DRAMATIQ.REDIS_HOST is not None:
        broker = RedisBroker(host=config.DRAMATIQ.REDIS_HOST)
    else:
        raise RuntimeError("Running a non-test environment without Redis host set")
    broker.add_middleware(AsyncIO())
    set_broker(broker)
