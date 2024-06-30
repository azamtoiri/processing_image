from contextlib import asynccontextmanager
from typing import AsyncIterator

import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from loguru import logger
from retry import retry

from src.utils.config import Connection


async def get_redis_connection():
    try:
        connection = await aioredis.from_url(
            Connection.CELERY_BROKER_URL,
        )
        logger.info("Connected to Redis")
        return connection
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return None


@retry(TypeError, tries=5, delay=5)
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Запущен инициализатор при сервере")
    FastAPICache.init(Connection.CELERY_BROKER_URL, prefix="fastapi-cache")
    connection = await get_redis_connection()
    app.state.redis_connection = connection
    yield
    # закрыть подключение к брокеру
    await connection.close()
