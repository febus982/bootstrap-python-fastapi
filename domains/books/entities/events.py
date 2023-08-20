import typing

import pydantic

from domains.books.entities.cloudevent_base import (
    BaseEvent,
    dataschema_field,
    type_field,
)


class BookCreatedV1Data(pydantic.BaseModel):
    book_id: int
    title: str
    author_name: str


class BookCreatedV1(BaseEvent):
    type: typing.Literal["book.created.v1"] = type_field("book.created.v1")
    dataschema: str = dataschema_field("book.created.v1")

    data: BookCreatedV1Data
