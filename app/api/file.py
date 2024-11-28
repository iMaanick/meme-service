from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.adapters.minio.gateway import MinioGateway
from app.application.models.file import UploadFileResponse, DeleteFileResponse, GetFileUrlResponse
from app.application.protocols.database import S3StorageGateway

private_router = APIRouter(prefix="/files")


@private_router.post("/", response_model=UploadFileResponse)
async def upload_file(
        minio_client: MinioGateway = Depends(S3StorageGateway),
        file: UploadFile = File(...)
) -> UploadFileResponse:
    filename = await minio_client.upload_file(file)

    if not filename:
        raise HTTPException(status_code=400, detail="Failed to upload the file.")

    return UploadFileResponse(detail="File uploaded successfully", filename=filename)


@private_router.delete("/", response_model=DeleteFileResponse)
async def delete_file(
        filename: str,
        minio_client: MinioGateway = Depends(MinioGateway),
) -> DeleteFileResponse:
    result = await minio_client.delete_file(filename)
    if not result:
        raise HTTPException(status_code=404, detail="File not found or could not be deleted.")
    return DeleteFileResponse(detail=result)


@private_router.get("/file-url/{filename}", response_model=GetFileUrlResponse)
async def get_file_url(
        filename: str,
        minio_client: MinioGateway = Depends(MinioGateway)
) -> GetFileUrlResponse:
    file_url = await minio_client.get_file_url(filename)
    if not file_url:
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found or could not generate URL.")
    return GetFileUrlResponse(file_url=file_url)

