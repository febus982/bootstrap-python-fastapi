from pydantic import BaseModel

from cloudevents.pydantic import CloudEvent
from . import models


class BookCreatedV1Data(BaseModel):
    book_id: int
    title: str
    author_name: str

    class Config:
        orm_mode = True


class BookCreatedV1(CloudEvent):
    def __init__(self, model: models.BookModel):
        _attrs = dict(
            type="book.created.v1",

            # url to GET endpoint (not implemented in this example)
            source="this.service.name",

            # url to data schema
            dataschema="this.service.tld/events/dataschema/book.created.v1",
        )

        super().__init__(attributes=_attrs, data=BookCreatedV1Data.from_orm(model))
