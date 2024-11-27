import datetime
from abc import ABC, abstractmethod
from typing import Optional

from app.application.models.meme import MemeCreate, Meme


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

