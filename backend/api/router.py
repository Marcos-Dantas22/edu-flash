from fastapi import APIRouter
from modules.auth.routes import router as auth_router

routers = APIRouter()

routers.include_router(auth_router, prefix="/auth", tags=["Auth"])
