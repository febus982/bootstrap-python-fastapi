from logging import getLogger
import socket

from confluent_kafka import Consumer, KafkaError, KafkaException

from common.bootstrap import application_init
from common.config import AppConfig


class KafkaConsumer:
    def __init__(self, app_config: AppConfig):
        conf = {
            "bootstrap.servers": app_config.KAFKA_BOOTSTRAP_SERVERS,
            "group.id": f"{app_config.APP_NAME}-{socket.gethostname()}",
            "auto.offset.reset": "smallest",
        }

        self._consumer = Consumer(conf)
        self._topics = [app_config.KAFKA_CONSUMER_TOPIC]
        self._running = False
        self._logger = getLogger()

    def consume_messages(self):
        self._running = True
        try:
            self._consumer.subscribe(self._topics)

            while self._running:
                msg = self._consumer.poll(timeout=1.0)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        self._logger.info("Reached end of offset")
                        # sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                        #                  (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    self._logger.info(f"Received message: {msg.value}")
        finally:
            # Close down consumer to commit final offsets.
            self._consumer.close()


def run_consumer(app_config: AppConfig):
    application_init(app_config)
    logger = getLogger()
    if not all(
        [
            app_config.KAFKA_CONSUMER_TOPIC,
            app_config.KAFKA_BOOTSTRAP_SERVERS,
        ]
    ):
        logger.error("Cannot start consumer without configuration")
        exit(1)

    consumer = KafkaConsumer(app_config)
    consumer.consume_messages()
