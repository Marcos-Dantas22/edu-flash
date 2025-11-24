
from fastapi import Request
from core.config import settings  # config do projeto
from fastapi.responses import JSONResponse

async def validate_api_key(request: Request, call_next):
    public_paths = [
        "/docs",
        "/redoc",
        "/openapi.json",
        "/docs/oauth2-redirect",
        "/favicon.ico",
    ]

    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)

    api_key = request.headers.get("X-API-Key")

    if api_key != settings.API_KEY:
        return JSONResponse(
            status_code=401,
            content={
                "errors": {
                    "api_key": ["API Key inválida ou ausente"]
                }
            }
        )

    return await call_next(request)
