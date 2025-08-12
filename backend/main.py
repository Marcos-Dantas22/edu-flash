# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import routers
from core.config import settings  # config do projeto

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