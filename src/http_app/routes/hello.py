from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from http_app.templates import templates

router = APIRouter(prefix="/hello")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def hello(request: Request):
    return templates.TemplateResponse("list_books.html", {"request": request})
