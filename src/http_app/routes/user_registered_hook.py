import logging

from fastapi import APIRouter, Request

router = APIRouter(prefix="/user_registered")


@router.post("/")
async def user_registered(request: Request):
    logging.info("User registered", extra={"body": await request.json()})
    return {"user_registered": "OK"}
