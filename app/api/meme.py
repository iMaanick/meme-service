from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.meme import add_meme, update_meme_by_id
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
async def update_organization(
        meme_id: int,
        meme_data: MemeUpdate,
        database: Annotated[DatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> UpdateMemeResponse:

    updated_meme_id = await update_meme_by_id(meme_id, meme_data, database, uow)
    if not updated_meme_id:
        raise HTTPException(status_code=404, detail="Meme not found")
    return UpdateMemeResponse(detail="Meme updated successfully")
