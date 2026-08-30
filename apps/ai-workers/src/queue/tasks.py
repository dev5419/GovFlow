"""
GovFlow Celery Tasks Initialization
Broker and result backend configured with Redis per techstack.md.
"""

from celery import Celery
from src.shared.config import settings

celery_app = Celery(
    "govflow_workers",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

# Standard alias for Celery CLI auto-discovery
app = celery_app
