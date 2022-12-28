from dependency_injector.wiring import Provide, inject
from sqlalchemy_bind_manager import SQLAlchemyRepository, SQLAlchemyBindManager

from app.domains.books._local import BookRepositoryInterface, BookModel


class BookRepository(SQLAlchemyRepository[BookModel], BookRepositoryInterface):
    _model = BookModel

    @inject
    def __init__(
            self,
            sa_manager: SQLAlchemyBindManager = Provide[SQLAlchemyBindManager.__name__],
    ) -> None:
        super().__init__(sa_manager)
