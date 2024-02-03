from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

router = APIRouter()


class PingResponse(BaseModel):
    ping: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ping": "pong!",
            }
        }
    )


@router.get("/ping")
async def ping() -> PingResponse:
    return PingResponse(ping="pong!")
