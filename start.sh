#!/bin/sh
# Ждём Postgres
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "⏳  waiting for db…"
  sleep 2
done

# Миграции
alembic upgrade head

# Запускаем FastAPI
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
