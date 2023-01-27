from dependency_injector.wiring import Provide, inject
from sqlalchemy_bind_manager import SQLAlchemyAsyncRepository, SQLAlchemyBindManager
from sqlalchemy_bind_manager._bind_manager import SQLAlchemyAsyncBind
from sqlalchemy_bind_manager.exceptions import UnsupportedBind

from domains.books._local import BookModel


class BookRepository(SQLAlchemyAsyncRepository[BookModel]):
    _model = BookModel

    @inject
    def __init__(
        self,
        sa_manager: SQLAlchemyBindManager = Provide[SQLAlchemyBindManager.__name__],
    ) -> None:
        bind = sa_manager.get_bind()
        """
        get_bind can return both sync and async binds, while the repository accepts only
        async ones. Typing or implementation improvements are necessary, in the meanwhile
        we verify the proper bind is passed in to be type safe.
        """
        if not isinstance(bind, SQLAlchemyAsyncBind):
            raise UnsupportedBind(
                "Submitted bind is not a SQLAlchemyAsyncBind instance"
            )
        super().__init__(bind)
