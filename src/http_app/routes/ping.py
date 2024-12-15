from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from starlette.responses import JSONResponse

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
    JSONResponse({"ping": "pong!"})
    return PingResponse(ping="pong!")
