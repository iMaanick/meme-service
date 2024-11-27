from dataclasses import dataclass

from fastapi import APIRouter, Request

index_router = APIRouter()


@dataclass
class IndexResponse:
    documentation: str


@index_router.get("/", response_model=IndexResponse)
async def index() -> IndexResponse:
    """
    Provides a link to the API documentation.
    """
    return IndexResponse(documentation="http://localhost:8000/docs")

