from typing import Optional

from app.application.models import MemeCreate, Meme, MemeUpdate
from app.application.protocols.database import DatabaseGateway, UoW


async def add_meme(
        meme_data: MemeCreate,
        database: DatabaseGateway,
) -> Meme:
    meme = await database.add_meme(meme_data)
    return meme


async def update_meme_by_id(
        meme_id: int,
        meme_data: MemeUpdate,
        database: DatabaseGateway,
        uow: UoW,
) -> Optional[int]:
    updated_meme_id = await database.update_meme_by_id(meme_id, meme_data)
    await uow.commit()
    return updated_meme_id


async def get_meme_data(
        meme_id: int,
        database: DatabaseGateway,
) -> Optional[Meme]:
    meme = await database.get_meme_by_id(meme_id)
    return meme


async def get_memes_data(
        skip: int,
        limit: int,
        database: DatabaseGateway,
) -> list[Meme]:
    memes = await database.get_memes(skip, limit)
    return memes
