from celery.utils.log import get_task_logger
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.celery_app import celery_app
from app.database.models.image_model import \
    Image as ImageModel  # предположим, что модели данных определены в этом модуле
from app.processing.image_process import resize_image
from app.utils.config import S3Connection, Connection
from app.utils.s3_client import S3Client

logger = get_task_logger(__name__)

# Конфигурация подключения к базе данных
engine = create_async_engine(f'{Connection.DATABASE_URL}/{Connection.DATABASE}')
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Конфигурация подключения к S3
s3_client = S3Client(
    access_key=S3Connection.ACCESS_KEY,
    secret_key=S3Connection.SECRET_KEY,
    bucket_name=S3Connection.BUCKET_NAME
)

S3_BUCKET_NAME = "your-s3-bucket-name"


@celery_app.task(name="tasks.process_image_task")
async def process_image_task(image_id, image_data):
    sizes = {
        "thumb": (150, 120),
        "big_thumb": (700, 700),
        "big_1920": (1920, 1080),
        "d2500": (2500, 2500)
    }

    async def update_image_status(image_id, status, versions=None):
        async with async_session() as session:
            async with session.begin():
                image = await session.get(ImageModel, image_id)
                if image:
                    image.status = status
                    if versions:
                        image.versions = versions
                    await session.commit()

    try:
        # Обработка изображений
        versions = {}
        for version, size in sizes.items():
            resized_image = resize_image(image_data, size)
            s3_key = f"images/{image_id}/{version}.jpg"
            await s3_client.upload_file(file_path=resized_image)
            versions[version] = s3_key

        # Обновление статуса изображения в базе данных
        await update_image_status(image_id, "done", versions)

    except Exception as e:
        logger.error(f"Error processing image {image_id}: {e}")
        await update_image_status(image_id, "error")
