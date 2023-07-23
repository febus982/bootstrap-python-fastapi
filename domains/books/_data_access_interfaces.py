from collections.abc import Iterable, Mapping
from typing import Any, List, Protocol, Tuple, Union

from cloudevents.pydantic import CloudEvent
from sqlalchemy_bind_manager.repository import SortDirection

from .entities.models import BookModel


class BookRepositoryInterface(Protocol):
    async def save(self, book: BookModel) -> BookModel:
        ...

    async def find(
        self,
        search_params: Union[None, Mapping[str, Any]] = None,
        order_by: Union[None, Iterable[Union[str, Tuple[str, SortDirection]]]] = None,
    ) -> List[BookModel]:
        ...


class BookEventGatewayInterface(Protocol):
    async def emit(self, event: CloudEvent) -> None:
        ...
