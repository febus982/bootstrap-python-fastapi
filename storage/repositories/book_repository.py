from dependency_injector.wiring import Provide, inject
from sqlalchemy_bind_manager import SQLAlchemyAsyncRepository, SQLAlchemyBindManager

from domains.books._local import BookModel


class BookRepository(SQLAlchemyAsyncRepository[BookModel]):
    _model = BookModel

    @inject
    def __init__(
        self,
        sa_manager: SQLAlchemyBindManager = Provide[SQLAlchemyBindManager.__name__],
    ) -> None:
        super().__init__(sa_manager.get_bind())  # type: ignore
