from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Minha API EDU FLASH"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Documentação da minha API"
    DATABASE_URL: str  
    TEST_DATABASE_URL: str

    class Config:
        env_file = ".env"  
        extra = "ignore" 

settings = Settings()

# if os.getenv("ENV") == "test":
#     settings = Settings(_env_file=".env.test")
# else:
#     settings = Settings()