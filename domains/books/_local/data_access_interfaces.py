from collections.abc import Iterable
from typing import Protocol, Union, Tuple

from sqlalchemy_bind_manager import SortDirection

from .models import BookModel


class BookRepositoryInterface(Protocol):
    def save(self, book: BookModel) -> BookModel:
        ...

    def find(
        self,
        order_by: Union[None, Iterable[Union[str, Tuple[str, SortDirection]]]] = None,
        **search_params,
    ) -> Iterable[BookModel]:
        ...
