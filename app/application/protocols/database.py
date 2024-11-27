from abc import ABC, abstractmethod
from typing import Optional

from app.application.models.meme import MemeCreate, Meme, MemeUpdate


class UoW(ABC):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def flush(self) -> None:
        raise NotImplementedError


class DatabaseGateway(ABC):

    @abstractmethod
    async def add_meme(self, price_data: MemeCreate) -> Meme:
        raise NotImplementedError

    @abstractmethod
    async def get_memes(self, skip: int, limit: int) -> list[Meme]:
        raise NotImplementedError

    @abstractmethod
    async def get_meme_by_id(self, meme_id: int) -> Optional[Meme]:
        raise NotImplementedError

    @abstractmethod
    async def update_meme_by_id(self, meme_id: int, meme_data: MemeUpdate) -> Optional[int]:
        raise NotImplementedError

