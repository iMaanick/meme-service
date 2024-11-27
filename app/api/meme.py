from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.meme import add_meme
from app.application.models import MemeCreate, Meme
from app.application.protocols.database import DatabaseGateway

meme_router = APIRouter()


@meme_router.post("/", response_model=Meme)
async def create_meme(
        meme_data: MemeCreate,
        database: Annotated[DatabaseGateway, Depends()],
) -> Meme:
    meme = await add_meme(meme_data, database)
    return meme
