from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class PingResponse(BaseModel):
    ping: str

    class Config:
        json_schema_extra = {
            "example": {
                "ping": "pong!",
            }
        }


@router.get("/ping", response_model=PingResponse)
async def ping() -> PingResponse:
    return PingResponse(ping="pong!")
