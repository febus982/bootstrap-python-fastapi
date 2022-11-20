from dataclasses import dataclass


@dataclass
class BookModel:
    title: str
    author_name: str
    book_id: int | None = None
