"""
GovFlow AI Workers Configuration Settings
"""

import os
from pydantic import BaseModel


class WorkerSettings(BaseModel):
    environment: str = os.getenv("ENVIRONMENT", "development")

    # Database (PostgreSQL 15)
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://govflow:govflow_secret@localhost:5432/govflow",
    )

    # Task Queue Broker & Result Backend (Redis 7)
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Object Storage (MinIO S3-compatible)
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    minio_bucket: str = os.getenv("MINIO_BUCKET", "govflow-documents")
    minio_secure: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"


settings = WorkerSettings()
