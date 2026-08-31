from celery import Celery
from src.config.settings import settings

celery_app = Celery(
    "api_gateway",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.task_routes = {
    "ingestion.*": {"queue": "celery"},
}
