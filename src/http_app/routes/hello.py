from fastapi import APIRouter, Request, Security
from fastapi.responses import HTMLResponse

from http_app.templates import templates

from .auth import decode_jwt

router = APIRouter(prefix="/hello")


@router.get("/", response_class=HTMLResponse, include_in_schema=True)
async def hello(request: Request, jwt_token=Security(decode_jwt)):
    return templates.TemplateResponse(
        name="hello.html",
        request=request,
        context={"token_payload": jwt_token},
    )
