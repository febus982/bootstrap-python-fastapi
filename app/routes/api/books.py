from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi_versionizer import api_version
from pydantic import BaseModel

from app.domains.books import BookServiceInterface, Book
from app.domains.books.dto import BookData

router = APIRouter(prefix="/books")


class CreateBookResponse(BaseModel):
    book: Book


"""
The views defined here have the functionalities of two components:

- Controller: transforms data coming from the HTTP Request into
              the data model required to use the application logic

- Presenter:  transforms the data coming from the application logic
              into the format needed for the proper HTTP Response
"""


@api_version(1)
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


# Example v2 API with added parameter
@api_version(2)
@router.post("/", response_model=CreateBookResponse)
@inject
async def create_book(
    data: BookData,
    some_optional_query_param: bool = False,
    book_service: BookServiceInterface = Depends(
        Provide[BookServiceInterface.__name__]
    ),
) -> CreateBookResponse:
    created_book = book_service.create_book(book=data)
    return CreateBookResponse(book=created_book)
