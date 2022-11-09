from dataclasses import dataclass


@dataclass
class Book:
    title: int
    author_name: str
    book_id: int = None
