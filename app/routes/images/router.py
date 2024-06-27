from msilib.schema import File

from fastapi import APIRouter, Depends, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine.session_maker import DatabaseSessionManager
from app.database.models import Image
from app.routes.images.schemas import ImageUploadResponse
from app.routes.websocket import router as websocket_router
from app.tasks import process_image_task
from app.utils.config import Connection

router = APIRouter()


# Зависимость для получения асинхронной сессии БД
async def get_db():
    async with DatabaseSessionManager(f'{Connection.DATABASE_URL}/{Connection.DATABASE}') as db_session:
        yield db_session


# Загрузка изображения и инициализация задачи Celery
@router.post("/", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File, project_id: int = None, db: AsyncSession = Depends(get_db)):
    # Здесь нужно сохранить изображение в S3 и получить URL
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are supported.")

    # Например, можно использовать boto3 для работы с S3

    # Создаем запись о загрузке изображения в базе данных
    db_image = Image(filename=file.filename, project_id=project_id, status="uploaded")
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)

    # Запуск задачи Celery для обработки изображения
    image_data = await file.read()
    process_image_task.delay(db_image.id, image_data)

    return {"upload_link": f"s3://{S3_BUCKET_NAME}/images/{db_image.id}/original.jpg"}


router.include_router(websocket_router)
