from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Minha API EDU FLASH"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Documentação da minha API"

    DATABASE_URL: str  # Ex: postgresql+psycopg2://user:pass@host:port/db

    class Config:
        env_file = ".env"  # Carrega variáveis do arquivo .env

settings = Settings()
