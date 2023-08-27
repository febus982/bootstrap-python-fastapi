import asyncio
import signal
from logging import getLogger

from common.config import AppConfig
from stream_consumer import consume_messages

# Event will be set if the program needs to stop
shutdown_event = asyncio.Event()


def signal_handler(*_):
    logger = getLogger()
    logger.info("Application received shutdown signal. Stopping...")
    shutdown_event.set()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

asyncio.run(consume_messages(AppConfig(), shutdown_event))
