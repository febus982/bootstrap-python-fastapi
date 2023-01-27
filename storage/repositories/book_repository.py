from sqlalchemy_bind_manager import SQLAlchemyAsyncRepository

from domains.books._local import BookModel


class BookRepository(SQLAlchemyAsyncRepository[BookModel]):
    _model = BookModel
