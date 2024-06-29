#!/bin/sh
# migration.sh

# Создание новой ревизии
#alembic revision --autogenerate -m "Initial tables"

# Применение миграций
alembic upgrade head

python app/main.py