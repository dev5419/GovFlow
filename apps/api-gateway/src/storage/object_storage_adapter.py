import io
from minio import Minio
from minio.error import S3Error
from src.config.settings import settings


class ObjectStorageAdapter:
    def __init__(self):
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
        self.bucket = settings.minio_bucket
        try:
            self._ensure_bucket_exists()
        except Exception as err:
            print(f"Warning: Could not connect to MinIO on init: {err}")

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        except S3Error as err:
            print(f"MinIO bucket error: {err}")

    def upload_file(self, file_name: str, file_data: bytes, content_type: str = "application/octet-stream") -> str:
        """
        Uploads raw file bytes to MinIO.
        Returns the object path inside the bucket.
        """
        try:
            self.client.put_object(
                self.bucket,
                file_name,
                data=io.BytesIO(file_data),
                length=len(file_data),
                content_type=content_type,
            )
            return file_name
        except S3Error as err:
            print(f"Error uploading file to MinIO: {err}")
            raise err

    def get_client(self) -> Minio:
        return self.client
