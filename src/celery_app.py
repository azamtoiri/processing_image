from celery import Celery

from src.utils.config import Connection

celery_app = Celery(
    "tasks",
    broker=Connection.CELERY_BROKER_URL,
    backend=Connection.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

import src.tasks
