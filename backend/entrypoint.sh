#!/bin/bash
set -e

echo "🔄 Aguardando banco de dados ficar disponível..."

# Extrai as variáveis do .env se necessário
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Espera o Postgres responder
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
  echo "⏳ Banco ainda não está pronto — tentando novamente..."
  sleep 2
done

echo "✅ Banco de dados disponível! Rodando migrações Alembic..."

# Roda as migrações
alembic upgrade head

echo "🚀 Iniciando servidor FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
