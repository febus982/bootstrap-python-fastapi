from collections.abc import Iterable, Mapping
from typing import Any, List, Protocol, Tuple, Union

from sqlalchemy_bind_manager.repository import SortDirection

from domains.books._models import BookModel
from domains.common.cloudevent_base import BaseEvent


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
    async def emit(self, event: BaseEvent) -> None:
        ...
