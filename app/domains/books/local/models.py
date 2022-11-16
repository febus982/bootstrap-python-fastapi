from dataclasses import dataclass


@dataclass
class BookModel:
    title: int
    author_name: str
    book_id: int | None = None
