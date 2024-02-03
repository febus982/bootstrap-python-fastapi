import typing

import pydantic
from pydantic import ConfigDict

from domains.common.cloudevent_base import (
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

    # The first example is used to generate the OpenAPI documentation!
    # Examples ate good! Add examples!
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "source": "this.service.url.here",
                    "type": "book.created.v1",
                    "dataschema": "book.created.v1/some_event",
                    "datacontenttype": "text/xml",
                    "subject": "123",
                    "data": {"book_id": 0, "title": "string", "author_name": "string"},
                    "id": "A234-1234-1234",
                    "specversion": "1.0",
                    "time": "2018-04-05T17:31:00Z",
                }
            ]
        }
    )
