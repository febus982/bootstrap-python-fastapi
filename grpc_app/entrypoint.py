import logging
import time
from concurrent import futures

import grpc
from dependency_injector.providers import Object

from config import AppConfig
from di_container import Container
from grpc_app.generated.books_pb2_grpc import add_BooksServicer_to_server
from grpc_app.services.books import BooksService
from storage import init_storage

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def grpc_server():
    Container(  # type: ignore
        config=Object(AppConfig()),
    )
    init_storage()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Register service
    add_BooksServicer_to_server(BooksService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    logging.info("GRPC started")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        logging.debug("GRPC stop")
        server.stop(0)


if __name__ == "__main__":
    grpc_server()
