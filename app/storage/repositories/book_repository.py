from app.domains.books.local import BookRepositoryInterface, BookModel
from .abstract import SQLAlchemyRepository


class BookRepository(BookRepositoryInterface, SQLAlchemyRepository):
    def create_book(
        self,
        book: BookModel,
    ) -> BookModel:
        with self.sa_manager.get_session() as session:
            session.add(book)
            session.commit()

        return book
