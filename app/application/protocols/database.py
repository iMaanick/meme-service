from abc import ABC, abstractmethod
from typing import Optional

from fastapi import UploadFile

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
    async def add_meme(self, description: str, filename: str, image_url: str) -> Meme:
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

    @abstractmethod
    async def delete_meme_by_id(self, meme_id: int) -> Optional[int]:
        raise NotImplementedError


class S3StorageGateway(ABC):

    @abstractmethod
    async def upload_file(self, file: UploadFile) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    async def delete_file(self, file_name: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    async def get_file_url(self, file_name: str) -> str:
        raise NotImplementedError
