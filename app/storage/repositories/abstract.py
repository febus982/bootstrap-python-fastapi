from abc import ABC

from dependency_injector.wiring import Provide, inject

from app.deps.sqlalchemy_manager import SQLAlchemyManager


class SQLAlchemyRepository(ABC):
    sa_manager: SQLAlchemyManager

    @inject
    def __init__(
            self,
            sa_manager: SQLAlchemyManager = Provide[SQLAlchemyManager.__name__]
    ) -> None:
        super().__init__()
        self.sa_manager = sa_manager
