from celery.result import AsyncResult
from fastapi import APIRouter, Depends, UploadFile, Body
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine.session_maker import DatabaseSessionManager
from app.database.models import Image
from app.routes.images import schemas
from app.routes.websocket import router as websocket_router
from app.tasks import process_image_task, test_process_image
from app.utils.config import Connection

router = APIRouter()


# Зависимость для получения асинхронной сессии БД
async def get_db():
    db = DatabaseSessionManager(f'{Connection.DATABASE_URL}/{Connection.DATABASE}')
    async with db.session_scope() as db_session:
        yield db_session


@router.post("/tasks", status_code=201)
def run_task(payload=Body(...)):
    task_type = payload["type"]
    task = test_process_image.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


# Загрузка изображения и инициализация задачи Celery
@router.post("/", response_model=schemas.ImageUpload)
async def upload_image(file: UploadFile, project_id: int = None, db: AsyncSession = Depends(get_db)):
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
    process_task = process_image_task.delay(db_image.id, image_data)

    return JSONResponse({"process_id": process_task.id})


@router.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)


router.include_router(websocket_router)
