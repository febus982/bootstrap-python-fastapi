from domains.books import dto, service


async def list_books():
    book_service = service.BookService()
    books = await book_service.list_books()
    return [dto.Book(**x.dict()) for x in books]
