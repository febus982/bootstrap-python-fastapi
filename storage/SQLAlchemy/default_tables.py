from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy_bind_manager import SQLAlchemyBind

from domains.books._local.models import BookModel


def init_tables(bind: SQLAlchemyBind):
    books = Table(
        "books",
        bind.registry_mapper.metadata,
        Column("book_id", Integer, primary_key=True),
        Column("title", String(50)),
        Column("author_name", String(50)),
    )
    bind.registry_mapper.map_imperatively(BookModel, books)
