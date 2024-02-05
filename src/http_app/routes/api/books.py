from domains.books import BookService, dto
from fastapi import APIRouter, status
from pydantic import BaseModel, ConfigDict

router_v1 = APIRouter(prefix="/books/v1")
router_v2 = APIRouter(prefix="/books/v2")


class CreateBookResponse(BaseModel):
    book: dto.Book
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author_name": "Douglas Adams",
                "book_id": 123,
            }
        }
    )


class CreateBookRequest(BaseModel):
    title: str
    author_name: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author_name": "Douglas Adams",
            }
        }
    )


"""
The views defined here have the functionalities of two components:

- Controller: transforms data coming from the HTTP Request into
              the data model required to use the application logic

- Presenter:  transforms the data coming from the application logic
              into the format needed for the proper HTTP Response
"""


@router_v1.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(
    data: CreateBookRequest,
) -> CreateBookResponse:
    book_service = BookService()
    created_book = await book_service.create_book(
        book=dto.BookData.model_validate(data, from_attributes=True)
    )
    return CreateBookResponse(book=created_book)


@router_v2.post("/", status_code=status.HTTP_201_CREATED)
async def create_book_v2(
    data: CreateBookRequest,
    some_optional_query_param: bool = False,
) -> CreateBookResponse:
    book_service = BookService()
    created_book = await book_service.create_book(
        book=dto.BookData.model_validate(data, from_attributes=True)
    )
    return CreateBookResponse(book=created_book)
