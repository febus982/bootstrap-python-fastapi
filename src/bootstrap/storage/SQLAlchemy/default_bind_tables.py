from domains.books._models import BookModel
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import registry


def init_tables(registry_mapper: registry):
    books = Table(
        "books",
        registry_mapper.metadata,
        Column("book_id", Integer, primary_key=True),
        Column("title", String(50)),
        Column("author_name", String(50)),
    )
    registry_mapper.map_imperatively(BookModel, books)
