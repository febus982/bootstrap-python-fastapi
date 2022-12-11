from dataclasses import dataclass
from typing import Union


@dataclass
class BookModel:
    title: str
    author_name: str
    book_id: Union[int, None] = None
