from dataclasses import asdict

from fastapi import APIRouter
from pydantic import BaseModel

from app.models import Book
from app.services.books import BookService

router = APIRouter(prefix="/books")


class BookData(BaseModel):
    title: str
    author_name: str

    class Config:
        schema_extra = {
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author_name": "Douglas Adams",
            }
        }


class BookEntity(BookData):
    book_id: int

    class Config:
        schema_extra = {
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author_name": "Douglas Adams",
                "book_id": 123,
            }
        }


class CreateBookResponse(BaseModel):
    book: BookEntity


"""
The views defined here have the functionalities of two components:

- Controller: transforms data coming from the HTTP Request into
              the data model required to use the application logic

- Presenter:  transforms the data coming from the application logic
              into the format needed for the proper HTTP Response
"""


@router.post('/', response_model=CreateBookResponse)
async def create_book(data: BookData) -> CreateBookResponse:
    created_book = BookService().create_book(
        book=Book(**data.dict()),
    )
    return CreateBookResponse(
        book=BookEntity(**asdict(created_book))
    )
