import logging
from concurrent import futures
from typing import Optional

from grpc.aio import server
from dependency_injector.providers import Object

from config import AppConfig, init_logger
from di_container import Container
from grpc_app.generated.books_pb2_grpc import add_BooksServicer_to_server
from grpc_app.servicers.books import BooksServicer
from storage import init_storage


# TODO: Add asyncio support: https://stackoverflow.com/questions/38387443/how-to-implement-a-async-grpc-python-server
def create_server(test_config: Optional[AppConfig] = None):
    init_logger(test_config or AppConfig())
    if not test_config:
        c = Container(
            config=Object(test_config or AppConfig()),
        )
        c.wire(packages=["grpc_app"])
    init_storage()
    s = server(futures.ThreadPoolExecutor(max_workers=10))
    # Register service
    add_BooksServicer_to_server(BooksServicer(), s)
    s.add_insecure_port("[::]:50051")
    return s


async def main():  # pragma: no cover
    s = create_server()
    await s.start()
    await s.wait_for_termination()
    logging.info("GRPC started")
