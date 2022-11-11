from dataclasses import asdict

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.domains.books.local.models import BookModel
from app.domains.books import BookService

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
@inject
async def create_book(
        data: BookData,
        book_service: BookService = Depends(Provide[BookService.__name__])
) -> CreateBookResponse:
    created_book = book_service.create_book(
        book=BookModel(**data.dict()),
    )
    return CreateBookResponse(
        book=BookEntity(**asdict(created_book))
    )
