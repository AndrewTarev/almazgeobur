from celery import Celery
from src.core.config import settings

celery_app = Celery(
    "worker",
    backend=settings.celery.CELERY_RESULT_BACKEND,
    broker=settings.celery.CELERY_BROKER_URL,
)
