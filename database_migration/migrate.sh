#!/bin/sh
# migration.sh

# Создание новой ревизии
#alembic revision --autogenerate -m "Initial tables"

# Применение миграций
alembic upgrade head

python src/app/server_app_run.py