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
    updated_organization_id = await database.update_meme_by_id(meme_id, meme_data)
    await uow.commit()
    return updated_organization_id
