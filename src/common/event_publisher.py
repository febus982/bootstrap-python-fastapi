# from typing import Dict, Union
from typing import Optional

import structlog

from domains import event_registry

from .config import EventConfig

logger = structlog.getLogger(__name__)


def init_broker(config: EventConfig):

    if config.REGISTER_PUBLISHERS:
        register_publishers(config.SUBSCRIBER_TOPIC)



def register_publishers(topic: Optional[str] = None):
    if topic is not None and topic in event_registry.keys():
        logger.info(f"Registering publishers for topic {topic}")
    else:
        logger.info(f"Registering publishers for all topics")
