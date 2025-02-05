from typing import Annotated, Literal

import pydantic
from cloudevents_pydantic.events import CloudEvent
from cloudevents_pydantic.events.fields import metadata
from cloudevents_pydantic.events.fields.types import URI, URIReference
from pydantic import ConfigDict, Field


class BookCreatedV1Data(pydantic.BaseModel):
    book_id: int
    title: str
    author_name: str


def _dataschema_url(value: str) -> str:
    return f"https://this_service/dataschemas/{value}"


class BookCreatedV1(CloudEvent):
    source: Annotated[
        URIReference,
        Field(default="/book_service", validate_default=True),
        metadata.FieldSource,
    ]
    type: Annotated[Literal["book.created.v1"], Field(default="book.created.v1"), metadata.FieldType]
    dataschema: Annotated[
        URI,
        Field(default=_dataschema_url("book.created.v1"), validate_default=True),
        metadata.FieldDataSchema,
    ]

    data: BookCreatedV1Data

    # The first example is used to generate the OpenAPI documentation!
    # Examples are good! Add examples!
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "source": "this.service.url.here",
                    "type": "book.created.v1",
                    "dataschema": "/dataschemas/book.created.v1",
                    "datacontenttype": "application/json",
                    "subject": "123",
                    "data": {"book_id": 0, "title": "string", "author_name": "string"},
                    "id": "A234-1234-1234",
                    "specversion": "1.0",
                    "time": "2018-04-05T17:31:00Z",
                }
            ]
        }
    )


class BookUpdatedV1(CloudEvent):
    source: Annotated[
        URIReference,
        Field(default="/book_service", validate_default=True),
        metadata.FieldSource,
    ]
    type: Annotated[Literal["book.updated.v1"], Field(default="book.updated.v1"), metadata.FieldType]
    dataschema: Annotated[
        URI,
        Field(default=_dataschema_url("book.updated.v1"), validate_default=True),
        metadata.FieldDataSchema,
    ]

    # This is just an example, too lazy to use a different data class
    data: BookCreatedV1Data

    # The first example is used to generate the OpenAPI documentation!
    # Examples are good! Add examples!
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "source": "this.service.url.here",
                    "type": "book.updated.v1",
                    "dataschema": "/dataschemas/book.updated.v1",
                    "datacontenttype": "application/json",
                    "subject": "123",
                    "data": {"book_id": 0, "title": "string", "author_name": "string"},
                    "id": "A234-1234-1234",
                    "specversion": "1.0",
                    "time": "2018-04-05T17:31:00Z",
                }
            ]
        }
    )
