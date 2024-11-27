from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.sqlalchemy_db import models
from app.application.models.meme import MemeCreate, Meme
from app.application.protocols.database import DatabaseGateway


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_meme(self, meme_data: MemeCreate) -> Meme:
        new_meme = models.Meme(
            description=meme_data.description,
            image_url=meme_data.image_url,
        )
        self.session.add(new_meme)
        print(new_meme)
        await self.session.commit()
        return Meme.model_validate(new_meme)
