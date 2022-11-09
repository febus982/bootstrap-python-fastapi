from app.models import Book
from app.domains.books import BookRepositoryInterface
from .abstract import SQLAlchemyRepository


class BookRepository(BookRepositoryInterface, SQLAlchemyRepository):
    def create_book(
            self,
            book: Book,
    ) -> Book:
        with self.sa_manager.get_session() as session:
            session.add(book)
            session.commit()

        return book
