from datetime import timedelta
from minio.error import S3Error
from src.storage.object_storage_adapter import ObjectStorageAdapter
from src.config.settings import settings


class SignedUrlService:
    def __init__(self, adapter: ObjectStorageAdapter = None):
        self.adapter = adapter or ObjectStorageAdapter()
        self.client = self.adapter.get_client()
        self.bucket = settings.minio_bucket

    def generate_signed_get_url(self, object_name: str, expires_in_minutes: int = 60) -> str:
        """
        Generates a temporary, short-lived signed GET URL for an object in MinIO.
        Returns the presigned URL as a string.
        """
        try:
            url = self.client.presigned_get_object(
                self.bucket,
                object_name,
                expires=timedelta(minutes=expires_in_minutes)
            )
            return url
        except S3Error as err:
            print(f"Error generating presigned URL: {err}")
            raise err
