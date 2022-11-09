from dependency_injector.wiring import inject, Provide

from app.models import Book
from .interfaces import BookRepositoryInterface


class BookService:
    @inject
    def create_book(
            self,
            book: Book,
            book_repository: BookRepositoryInterface = Provide[BookRepositoryInterface.__name__]
    ) -> Book:
        return book_repository.create_book(book)
