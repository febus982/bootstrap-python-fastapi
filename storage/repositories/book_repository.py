from sqlalchemy_bind_manager.repository import SQLAlchemyAsyncRepository

from domains.books._models import BookModel


class BookRepository(SQLAlchemyAsyncRepository[BookModel]):
    _model = BookModel
