import pydantic_asyncapi as pa
from fastapi import APIRouter

schema = pa.AsyncAPIV3(
    id="http://aa.aa.aa",
    info=pa.v3.Info(
        title="Bookstore API",
        version="1.0.0",
        description="test",
    ),
)

router = APIRouter(prefix="/asyncapi")

@router.get("/asyncapi.json", response_model_exclude_unset=True)
def asyncapi_raw() -> pa.AsyncAPIV3:
    return schema

@router.get("/docs", response_model_exclude_unset=True)
def asyncapi_docs() -> pa.AsyncAPIV3:
    return schema

