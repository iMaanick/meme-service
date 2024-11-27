from app.application.models import MemeCreate, Meme
from app.application.protocols.database import DatabaseGateway


async def add_meme(
        meme_data: MemeCreate,
        database: DatabaseGateway,
) -> Meme:
    meme = await database.add_meme(meme_data)
    return meme
