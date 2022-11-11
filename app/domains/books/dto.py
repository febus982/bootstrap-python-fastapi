from pydantic import BaseModel


class Book(BaseModel):
    title: int
    author_name: str
    book_id: int = None
