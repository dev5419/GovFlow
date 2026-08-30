"""
GovFlow API Gateway Configuration Settings
"""

import os
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "GovFlow API Gateway"
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Database (PostgreSQL 15)
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://govflow:govflow_secret@localhost:5432/govflow",
    )

    # Cache & Task Queue Broker (Redis 7)
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Object Storage (MinIO S3-compatible)
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    minio_bucket: str = os.getenv("MINIO_BUCKET", "govflow-documents")
    minio_secure: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"

    # Security & Auth
    jwt_secret: str = os.getenv(
        "JWT_SECRET",
        "govflow_jwt_super_secret_key_change_in_production_min_32_bytes",
    )


settings = Settings()
