from app.domains.books._local import BookRepositoryInterface, BookModel
from .abstract import SQLAlchemyRepository


class BookRepository(BookRepositoryInterface, SQLAlchemyRepository):
    def create_book(
        self,
        book: BookModel,
    ) -> BookModel:
        # MyPy doesn't like session used as context manager
        with self.sa_manager.get_session() as session:  # type: ignore
            session.add(book)
            session.commit()

        return book
