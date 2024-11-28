from typing import Optional

from fastapi import UploadFile

from app.application.protocols.database import S3StorageGateway


async def save_file(
        file: UploadFile,
        storage: S3StorageGateway,
) -> Optional[str]:
    filename = await storage.upload_file(file)
    return filename


async def delete_file_by_filename(
        filename: str,
        storage: S3StorageGateway,
) -> Optional[str]:
    deleted_file_data = await storage.delete_file(filename)
    return deleted_file_data


async def get_url_by_filename(
        filename: str,
        storage: S3StorageGateway,
) -> Optional[str]:
    url = await storage.get_file_url(filename)
    return url
