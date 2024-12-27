from dramatiq import set_broker
from dramatiq.brokers.stub import StubBroker
from dramatiq.middleware import AsyncIO
from opentelemetry_instrumentor_dramatiq import DramatiqInstrumentor

from .config import AppConfig


def init_dramatiq(config: AppConfig):
    DramatiqInstrumentor().instrument()
    if config.ENVIRONMENT == "test":
        broker = StubBroker()
    else:
        broker = StubBroker()
    # broker.emit_after("process_boot")
    broker.add_middleware(AsyncIO())
    set_broker(broker)
