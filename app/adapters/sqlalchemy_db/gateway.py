from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.sqlalchemy_db import models
from app.application.models.meme import MemeCreate, Meme, MemeUpdate
from app.application.protocols.database import DatabaseGateway


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_meme(self, description: str, filename: str, image_url: str) -> Meme:
        new_meme = models.Meme(
            description=description,
            image_url=image_url,
            filename=filename
        )
        self.session.add(new_meme)
        await self.session.commit()
        return Meme.model_validate(new_meme)

    async def get_memes(self, skip: int, limit: int) -> list[Meme]:
        query = select(models.Meme).offset(skip).limit(limit)
        result = await self.session.execute(query)
        memes = [Meme.model_validate(meme) for meme in result.scalars().all()]
        return memes

    async def get_meme_by_id(self, meme_id: int) -> Optional[Meme]:
        query = select(models.Meme).where(models.Meme.id == meme_id)
        result = await self.session.execute(query)
        meme = result.scalars().first()
        if meme:
            return Meme.model_validate(meme)
        return None

    async def update_meme_by_id(self, meme_id: int, meme_data: MemeUpdate) -> Optional[int]:
        result = await self.session.execute(
            select(models.Meme).
            where(models.Meme.id == meme_id)
        )
        meme = result.scalars().first()
        if not meme:
            return None
        meme.description = meme_data.description
        meme.image_url = meme_data.image_url
        return meme.id

    async def delete_meme_by_id(self, meme_id: int) -> Optional[int]:
        result = await self.session.execute(
            select(models.Meme).where(models.Meme.id == meme_id))
        meme = result.scalars().first()
        if not meme:
            return None
        await self.session.delete(meme)
        return meme.id
