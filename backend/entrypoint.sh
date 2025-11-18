#!/bin/bash
set -e

echo "🔄 Aguardando banco de dados ficar disponível..."

# Extrai as variáveis do .env se necessário (com expansão de variáveis internas)
if [ -f .env ]; then
  set -o allexport
  source .env
  set +o allexport
fi

# valores padrão caso não estejam no .env
# : "${POSTGRES_HOST:=db}"
# : "${POSTGRES_PORT:=5432}"
# : "${POSTGRES_USER:=postgres}"
# : "${POSTGRES_DB:=postgres}"

# Função utilitária para checar conectividade
check_with_pg_isready() {
  pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" >/dev/null 2>&1
}

check_with_psql() {
  PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' >/dev/null 2>&1
}

# Tenta por até ~2 minutos (60 tentativas de 2s)
MAX_RETRIES=60
RETRY=0

while true; do
  if command -v pg_isready >/dev/null 2>&1; then
    if check_with_pg_isready; then
      break
    fi
  elif command -v psql >/dev/null 2>&1; then
    if check_with_psql; then
      break
    fi
  else
    # fallback: tenta abrir socket TCP (poderá passar mesmo que pg não esteja pronto)
    if (echo > /dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT) >/dev/null 2>&1; then
      break
    fi
  fi

  RETRY=$((RETRY+1))
  echo "⏳ Banco ainda não está pronto — tentando novamente... ($RETRY/$MAX_RETRIES)"
  if [ "$RETRY" -ge "$MAX_RETRIES" ]; then
    echo "❌ Timeout aguardando banco. Saindo."
    exit 1
  fi
  sleep 2
done

echo "✅ Banco de dados disponível! Rodando migrações Alembic..."

# Roda as migrações
alembic upgrade head

echo "🚀 Iniciando servidor FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
