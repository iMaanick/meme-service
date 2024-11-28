from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.application.file import save_file, delete_file_by_filename, get_url_by_filename, validate_image_file
from app.application.models.file import UploadFileResponse, DeleteFileResponse, GetFileUrlResponse
from app.application.protocols.database import S3StorageGateway

private_router = APIRouter(prefix="/files")


@private_router.post("/", response_model=UploadFileResponse)
async def upload_file(
        file: Annotated[UploadFile, Depends(validate_image_file)],
        storage: Annotated[S3StorageGateway, Depends()],
) -> UploadFileResponse:
    filename = await save_file(file, storage)
    if not filename:
        raise HTTPException(status_code=400, detail="Failed to upload the file.")
    return UploadFileResponse(detail="File uploaded successfully", filename=filename)


@private_router.delete("/", response_model=DeleteFileResponse)
async def delete_file(
        filename: str,
        storage: Annotated[S3StorageGateway, Depends()],
) -> DeleteFileResponse:
    result = await delete_file_by_filename(filename, storage)
    if not result:
        raise HTTPException(status_code=404, detail="File not found or could not be deleted.")
    return DeleteFileResponse(detail=result)


@private_router.get("/file-url/{filename}", response_model=GetFileUrlResponse)
async def get_file_url(
        filename: str,
        storage: Annotated[S3StorageGateway, Depends()],
) -> GetFileUrlResponse:
    file_url = await get_url_by_filename(filename, storage)
    if not file_url:
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found or could not generate URL.")
    return GetFileUrlResponse(file_url=file_url)

