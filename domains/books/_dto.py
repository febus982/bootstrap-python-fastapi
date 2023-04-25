from typing import Union

from pydantic import BaseModel


class BookData(BaseModel):
    title: str
    author_name: str

    class Config:
        orm_mode = True


class Book(BookData):
    book_id: Union[int, None] = None

    class Config:
        orm_mode = True
