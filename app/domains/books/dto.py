from pydantic import BaseModel


class BookData(BaseModel):
    title: str
    author_name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author_name": "Douglas Adams",
            }
        }


class Book(BookData):
    book_id: int | None = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author_name": "Douglas Adams",
                "book_id": 123,
            }
        }
