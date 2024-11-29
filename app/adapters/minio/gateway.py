import io
import os
import uuid
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import UploadFile

from app.application.protocols.database import S3StorageGateway


class MinioGateway(S3StorageGateway):
    def __init__(self):
        base_url = os.getenv("MINIO_URL", "http://localhost:9000")

        self.client = boto3.client(
            's3',
            endpoint_url=base_url,
            aws_access_key_id="minioadmin",
            aws_secret_access_key="minioadmin",
            region_name="us-east-1"
        )

        self.bucket_name = "memes-bucket"
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            self.client.create_bucket(Bucket=self.bucket_name)
            print(f"Bucket '{self.bucket_name}' created.")

    async def upload_file(self, file: UploadFile) -> Optional[str]:
        try:
            unique_filename = f"{uuid.uuid4()}_{file.filename}"
            file_data = await file.read()

            self.client.put_object(
                Bucket=self.bucket_name,
                Key=unique_filename,
                Body=io.BytesIO(file_data)
            )

            return unique_filename
        except (BotoCoreError, ClientError) as err:
            print(err)
            return None

    async def get_file_url(self, filename: str, expiration: int = 3600) -> Optional[str]:
        try:
            if not self.is_file_exists(filename):
                return None

            url: str = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': filename},
                ExpiresIn=expiration
            )
            return url.replace("minio:9000", "localhost:9000")
        except (BotoCoreError, ClientError) as err:
            print(err)
            return None

    async def delete_file(self, filename: str) -> Optional[str]:
        try:
            if not self.is_file_exists(filename):
                return None

            self.client.delete_object(Bucket=self.bucket_name, Key=filename)
            return f"File '{filename}' deleted successfully"
        except (BotoCoreError, ClientError) as err:
            print(err)
            return None

    def is_file_exists(self, filename: str) -> bool:
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=filename)
            return True
        except ClientError as err:
            print(err)
            return False
