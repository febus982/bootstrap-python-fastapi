from collections.abc import Iterable, Mapping
from typing import Protocol, Union, Tuple, List, Any

from sqlalchemy_bind_manager import SortDirection

from .models import BookModel


class BookRepositoryInterface(Protocol):
    async def save(self, book: BookModel) -> BookModel:
        ...

    async def find(
        self,
        search_params: Union[None, Mapping[str, Any]] = None,
        order_by: Union[None, Iterable[Union[str, Tuple[str, SortDirection]]]] = None,
    ) -> List[BookModel]:
        ...
