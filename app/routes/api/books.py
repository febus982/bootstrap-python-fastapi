from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.domains.books import BookServiceInterface, Book
from app.domains.books.dto import BookData

router = APIRouter(prefix="/api/books")


class CreateBookResponse(BaseModel):
    book: Book


"""
The views defined here have the functionalities of two components:

- Controller: transforms data coming from the HTTP Request into
              the data model required to use the application logic

- Presenter:  transforms the data coming from the application logic
              into the format needed for the proper HTTP Response
"""


@router.post("/", response_model=CreateBookResponse)
@inject
async def create_book(
    data: BookData,
    book_service: BookServiceInterface = Depends(
        Provide[BookServiceInterface.__name__]
    ),
) -> CreateBookResponse:
    created_book = book_service.create_book(book=data)
    return CreateBookResponse(book=created_book)
