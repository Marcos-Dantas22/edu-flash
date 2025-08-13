# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import routers
from core.config import settings  # config do projeto
import sentry_sdk

# Configurações do Sentry
# sentry_sdk.init(
#     dsn="https://5e2867ec4c045398f22da585757a61ef@o4509192557494272.ingest.us.sentry.io/4509833659351040",
#     # Add data like request headers and IP for users,
#     # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
#     send_default_pii=True,
# )

# Cria a aplicação FastAPI
app = FastAPI(
    title="Minha API",
    description="API para gerenciamento de dados",
    version="1.0.0",
    docs_url="/docs",        # URL do Swagger
    redoc_url="/redoc",      # URL do ReDoc
    openapi_url="/openapi.json"  # JSON do schema
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, colocar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrando rotas
app.include_router(routers, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# @app.get("/sentry-debug")
# async def trigger_error():
#     division_by_zero = 1 / 0