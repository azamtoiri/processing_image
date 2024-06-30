import asyncio

from celery.utils.log import get_task_logger

from src.celery_app import celery_app
from src.processing.image_process import resize_image
from src.utils.client import get_s3_client
from src.utils.config import components, S3Connection
from src.utils.image_size import get_image_size

logger = get_task_logger(__name__)

# S3 client configuration
s3_client = get_s3_client()


# Celery task for processing image
@celery_app.task(name="tasks.process_image_task")
def process_image_task(image_id, project_id, image_data):
    original_size = get_image_size(image_data)

    sizes = {
        "original": original_size,
        "big_thumb": (700, 700),
        "thumb": (150, 120),
        "big_1920": (1920, 1080),
        "d2500": (2500, 2500)
    }

    async def process():
        try:
            # Обработка изображений
            for version, size in sizes.items():
                if version == "original":
                    s3_key = f"images/{project_id}/{image_id}/{version}.jpg"
                    await s3_client.upload_binary(object_data=image_data, object_name=s3_key)
                resized_image = resize_image(image_data, size)
                s3_key = f"images/{project_id}/{image_id}/{version}.jpg"
                logger.info(f"Upload s3_key: {S3Connection.BUCKET_WEBSITE}/{s3_key}")
                await s3_client.upload_binary(object_data=resized_image, object_name=s3_key)
                await components.repositories_com.image_repository.update_image_version(
                    image_id, version,
                    f'{S3Connection.BUCKET_WEBSITE}/{s3_key}'
                )

            await components.repositories_com.image_repository.update_image_status(image_id, "done")
            return True

        except Exception as e:
            logger.error(f"Error processing image {image_id}: {e}")
            await components.repositories_com.image_repository.update_image_status(image_id, "error")
            return False

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(process())


if __name__ == '__main__':
    async def main():
        await components.repositories_com.image_repository.show_work()


    asyncio.run(main())
