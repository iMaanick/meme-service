from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.meme import add_meme, update_meme_by_id, get_meme_data, get_memes_data
from app.application.models import MemeCreate, Meme, MemeUpdate
from app.application.models.meme import UpdateMemeResponse
from app.application.protocols.database import DatabaseGateway, UoW

meme_router = APIRouter()


@meme_router.post("/", response_model=Meme)
async def create_meme(
        meme_data: MemeCreate,
        database: Annotated[DatabaseGateway, Depends()],
) -> Meme:
    meme = await add_meme(meme_data, database)
    return meme


@meme_router.put("/{meme_id}/", response_model=UpdateMemeResponse)
async def update_meme(
        meme_id: int,
        meme_data: MemeUpdate,
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> UpdateMemeResponse:
    updated_meme_id = await update_meme_by_id(meme_id, meme_data, database, uow)
    if not updated_meme_id:
        raise HTTPException(status_code=404, detail="Meme not found")
    return UpdateMemeResponse(detail="Meme updated successfully")


@meme_router.get("/{meme_id}", response_model=Meme)
async def get_meme(
        meme_id: int,
        database: Annotated[DatabaseGateway, Depends()],
) -> Meme:
    meme = await get_meme_data(meme_id, database)
    if not meme:
        raise HTTPException(status_code=404, detail="Data not found for specified meme_id.")
    return meme


@meme_router.get("/", response_model=list[Meme])
async def get_memes(
        database: Annotated[DatabaseGateway, Depends()],
        skip: int = 0,
        limit: int = 10,
) -> list[Meme]:
    memes = await get_memes_data(skip, limit, database)
    return memes
