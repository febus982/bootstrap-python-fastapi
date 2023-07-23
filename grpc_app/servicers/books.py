import grpc

import grpc_app.generated.books_pb2 as books_messages
import grpc_app.generated.books_pb2_grpc as books_grpc
from domains.books import service


class BooksServicer(books_grpc.BooksServicer):
    async def ListBooks(
        self,
        request: books_messages.ListBooksRequest,
        context: grpc.ServicerContext,
    ):
        book_service = service.BookService()
        return books_messages.ListBooksResponse(
            books=[
                books_messages.Book(**x.dict()) for x in await book_service.list_books()
            ]
        )
