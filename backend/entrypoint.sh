#!/bin/bash
set -e

# Roda as migrações do Alembic
alembic upgrade head

# Inicia o servidor FastAPI
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
