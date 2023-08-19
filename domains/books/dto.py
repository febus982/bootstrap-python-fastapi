from typing import Union

from pydantic import BaseModel


class BookData(BaseModel):
    title: str
    author_name: str


class Book(BookData):
    book_id: Union[int, None] = None
