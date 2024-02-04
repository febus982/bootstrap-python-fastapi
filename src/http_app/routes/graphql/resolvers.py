from domains.books import BookService, dto


async def list_books():
    book_service = BookService()
    books = await book_service.list_books()
    return [dto.Book.model_validate(x, from_attributes=True) for x in books]
