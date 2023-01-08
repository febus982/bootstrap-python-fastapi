import logging
from concurrent import futures

import grpc
from dependency_injector.providers import Object

from config import AppConfig
from di_container import Container
from grpc_app.generated.books_pb2_grpc import add_BooksServicer_to_server
from grpc_app.services.books import BooksService
from storage import init_storage


# TODO: Add asyncio support: https://stackoverflow.com/questions/38387443/how-to-implement-a-async-grpc-python-server
def create_server():
    Container(  # type: ignore
        config=Object(AppConfig()),
    )
    init_storage()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Register service
    add_BooksServicer_to_server(BooksService(), server)
    server.add_insecure_port("[::]:50051")
    return server
