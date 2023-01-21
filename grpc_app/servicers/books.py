import grpc
from dependency_injector.wiring import Provide, inject

import grpc_app.generated.books_pb2 as books_messages
import grpc_app.generated.books_pb2_grpc as books_grpc
from domains.books.boundary_interfaces import BookServiceInterface


class BooksServicer(books_grpc.BooksServicer):
    @inject
    async def ListBooks(
        self,
        request: books_messages.ListBooksRequest,
        context: grpc.ServicerContext,
        book_service: BookServiceInterface = Provide[BookServiceInterface.__name__],
    ):
        return books_messages.ListBooksResponse(
            books=[
                books_messages.Book(**x.dict()) for x in await book_service.list_books()
            ]
        )
