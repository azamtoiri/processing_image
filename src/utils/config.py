import asyncio
import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv

from src.database.engine.session_maker import DatabaseSessionManager
from src.database.models import Project
from src.database.repositories.storage_container import Repositories

load_dotenv()


class Connection:
    DATABASE_URL = os.getenv("POSTGRES_URL")
    DATABASE = os.getenv("DATABASE")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")


class S3Connection:
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    BUCKET_WEBSITE = os.getenv("BUCKET_WEBSITE")


@dataclass
class SystemComponents:
    repositories_com: Any


def initialize_database_session_manager(settings: Connection):
    database = f'{settings.DATABASE_URL}/{settings.DATABASE}'
    return DatabaseSessionManager(database_url=database)


def initialize_repositories_com(settings):
    session_manager = initialize_database_session_manager(settings)
    return Repositories(database_session_manager=session_manager)


def get_components(settings) -> SystemComponents:
    return SystemComponents(
        repositories_com=initialize_repositories_com(settings),
    )


components = get_components(settings=Connection)

if __name__ == '__main__':
    async def main():
        db_project = await components.repositories_com.project_repository.get_project(id=6)
        if not db_project:
            print("Нет добавлаяем")
            # Если проект не существует, создаем новый
            await components.repositories_com.project_repository.save(6)
        else:
            print("Нет не Добавили новый")

    asyncio.run(main())
