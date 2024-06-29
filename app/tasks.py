import asyncio

from celery.utils.log import get_task_logger

from app.celery_app import celery_app
from app.database.engine.session_maker import DatabaseSessionManager
from app.database.models.image_model import Image as ImageModel, ImageVersion
from app.database.repositories.image_repository import ImageRepository
from app.processing.image_process import resize_image
from app.utils.client import get_s3_client
from app.utils.config import Connection
from app.utils.image_size import get_image_size

logger = get_task_logger(__name__)

# Database connection configuration
database_url = f'{Connection.DATABASE_URL}/{Connection.DATABASE}'
database_session = DatabaseSessionManager(database_url=database_url)

# S3 client configuration
s3_client = get_s3_client()


# Celery task for processing image
@celery_app.task(name="tasks.process_image_task")
def process_image_task(image_id, image_data):
    original_size = get_image_size(image_data)
    repo = ImageRepository(db_session_manager=database_session)
    sizes = {
        "original": original_size,
        "thumb": (150, 120),
        "big_thumb": (700, 700),
        "big_1920": (1920, 1080),
        "d2500": (2500, 2500)
    }

    async def process():
        try:
            # Обработка изображений
            original_s3_url = None

            async with database_session.session_scope() as session:
                db_image = await session.get(ImageModel, image_id)
                if not db_image:
                    raise Exception(f"Image with id {image_id} not found in database")

                for version, size in sizes.items():
                    if version == "original":
                        s3_key = f"images/{image_id}/{version}.jpg"
                        await s3_client.upload_binary(object_data=image_data, object_name=s3_key)

                    resized_image = resize_image(image_data, size)
                    s3_key = f"images/{image_id}/{version}.jpg"
                    print(s3_key)
                    await s3_client.upload_binary(object_data=resized_image, object_name=s3_key)
                    await repo.update_image_version(image_id, version, s3_key)

                await repo.update_image_status(image_id, "done")
                # await websocket_endpoint.notify_image_ready(image_id, 11)

                return True

        except Exception as e:
            logger.error(f"Error processing image {image_id}: {e}")
            await repo.update_image_status(image_id, "error")
            return False

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(process())
