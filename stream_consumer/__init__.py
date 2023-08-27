import asyncio
from logging import getLogger

from aiokafka import AIOKafkaConsumer

from common.bootstrap import application_init
from common.config import AppConfig


async def consume_messages(
    app_config: AppConfig, shutdown_event: asyncio.Event
) -> None:
    application_init(app_config)
    logger = getLogger()
    if not all([
        app_config.KAFKA_CONSUMER_TOPIC,
        app_config.KAFKA_BOOTSTRAP_SERVERS,
    ]):
        logger.error("Cannot start consumer without configuration")
        exit(1)

    # This context manager takes care of start() and stop() calls
    async with AIOKafkaConsumer(
        app_config.KAFKA_CONSUMER.topic,
        bootstrap_servers=app_config.KAFKA_CONSUMER.bootstrap_servers,
        group_id=f"{app_config.APP_NAME}-{app_config.KAFKA_CONSUMER.topic}",
        # auto_offset_reset='earliest',
        enable_auto_commit=False,
    ) as consumer:
        logger.info("Consumer started")
        # We want to shutdown if event is triggered
        while not shutdown_event.is_set():
            # try to fetch a message with a timeout
            try:
                message = await asyncio.wait_for(consumer.getone(), timeout=1.0)
                logger.info(f"Received message: {message.value.decode('utf-8')}")
                await asyncio.sleep(10)
                await asyncio.wait_for(consumer.commit(), timeout=1.0)
                logger.info("Committed message")

            except asyncio.TimeoutError:
                # no message fetched within 1 second
                continue
