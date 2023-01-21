from collections.abc import AsyncIterable, Iterable
from typing import Protocol, Union, Tuple

from sqlalchemy_bind_manager import SortDirection

from .models import BookModel


class BookRepositoryInterface(Protocol):
    async def save(self, book: BookModel) -> BookModel:
        ...

    async def find(
        self,
        order_by: Union[None, Iterable[Union[str, Tuple[str, SortDirection]]]] = None,
        **search_params,
    ) -> AsyncIterable[BookModel]:
        ...
