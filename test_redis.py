# test_celery.py

from src.celery_app import celery_app
from src.tasks import process_image_task

if __name__ == "__main__":
    # Запуск тестовой задачи
    task = process_image_task.delay(1, b"test_image_data")

    # Ожидание выполнения задачи и получение результата
    result = task.get(timeout=10)
    print(f"Task result: {result}")
