import os
from concurrent import futures
from typing import Optional

from grpc.aio import server
from structlog import get_logger

from config import AppConfig, init_logger
from domains import init_celery, init_domains
from gateways.storage import init_storage
from grpc_app.generated.books_pb2_grpc import add_BooksServicer_to_server
from grpc_app.servicers.books import BooksServicer


async def create_server(test_config: Optional[AppConfig] = None):
    app_config = test_config or AppConfig()
    init_logger(app_config)
    init_domains(app_config)
    init_storage()
    init_celery(app_config)
    s = server(futures.ThreadPoolExecutor(max_workers=10))
    # Register service
    add_BooksServicer_to_server(BooksServicer(), s)
    address = "0.0.0.0:9999"
    logger = get_logger()
    await logger.ainfo(f"[{os.getpid()}] Listening on {address}")
    s.add_insecure_port(address)
    return s


async def main():  # pragma: no cover
    s = await create_server()
    await s.start()
    logger = get_logger()
    await logger.ainfo("GRPC started")
    await s.wait_for_termination()
