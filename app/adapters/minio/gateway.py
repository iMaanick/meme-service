import io
import uuid
from typing import Optional

from fastapi import UploadFile
from minio import Minio, S3Error

from app.application.protocols.database import S3StorageGateway


class MinioGateway(S3StorageGateway):
    def __init__(self):
        self.client = Minio(
            "localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            secure=False
        )

        self.bucket_name = "memes-bucket"
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
            print(f"Bucket '{self.bucket_name}' created.")

    async def upload_file(self, file: UploadFile) -> Optional[str]:
        try:
            unique_filename = f"{uuid.uuid4()}_{file.filename}"
            file_data = await file.read()

            self.client.put_object(self.bucket_name, unique_filename, io.BytesIO(file_data), len(file_data))

            return unique_filename
        except S3Error as err:
            print(err)
            return None

    async def get_file_url(self, filename: str) -> Optional[str]:
        try:
            if not self.is_file_exists(filename):
                return None
            return self.client.presigned_get_object(self.bucket_name, filename)
        except S3Error as err:
            print(err)
            return None

    async def delete_file(self, filename: str) -> Optional[str]:
        try:
            if not self.is_file_exists(filename):
                return None
            self.client.remove_object(self.bucket_name, filename)
            return f"File '{filename}' deleted successfully"
        except S3Error as err:
            print(err)
            return None

    def is_file_exists(self, filename: str) -> bool:
        try:
            self.client.stat_object(self.bucket_name, filename)
            return True
        except S3Error as err:
            return False
