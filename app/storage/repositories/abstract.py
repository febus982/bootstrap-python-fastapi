from abc import ABC

from dependency_injector.wiring import Provide, inject
from sqlalchemy_bind_manager import SQLAlchemyBindManager


class SQLAlchemyRepository(ABC):
    sa_manager: SQLAlchemyBindManager

    @inject
    def __init__(
        self,
        sa_manager: SQLAlchemyBindManager = Provide[SQLAlchemyBindManager.__name__],
    ) -> None:
        super().__init__()
        self.sa_manager = sa_manager
