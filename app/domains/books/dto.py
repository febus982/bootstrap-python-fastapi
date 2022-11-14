from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author_name: str
    book_id: int = None

    class Config:
        orm_mode = True
