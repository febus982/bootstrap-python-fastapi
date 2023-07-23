import typing

from ._dto import Book
from cloudevents import pydantic


class BookCreatedV1(pydantic.CloudEvent):
    def __init__(self, data: Book, attributes: typing.Optional[typing.Dict[str, typing.Any]] = None,
                 **kwargs):
        _attrs = dict(
            type="book.created.v1",

            # url to GET endpoint (not implemented in this example)
            source="this.service.tld/books",

            # url to data schema, perhaps produced using `Book.schema_json()` ?
            dataschema="this.service.tld/events/schemas/books",
        )
        if attributes:
            _attrs.update(attributes)
        super().__init__(_attrs, data.dict(), **kwargs)
