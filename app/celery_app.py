from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  # Брокер сообщений (например, Redis)
    backend="redis://localhost:6379/1"  # Бэкенд для хранения результатов задач (например, Redis)
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
