from typing import Optional

from fastapi import UploadFile, HTTPException, File

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


async def validate_image_file(file: UploadFile = File(...)) -> UploadFile:
    allowed_image_types = {"image/jpeg", "image/png", "image/gif"}
    if file.content_type not in allowed_image_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Only images are allowed."
        )
    return file
