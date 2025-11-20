from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Any

def _extract_field_from_loc(loc: Any) -> str:
    """Retorna o nome do campo a partir de loc (list/tuple/...).
    Ex: ['body','items',0,'name'] -> 'name'. Se não for possível, retorna 'non_field_errors'."""
    if isinstance(loc, (list, tuple)) and len(loc) > 0:
        # pega o último item legível como string
        last = loc[-1]
        try:
            return str(last)
        except Exception:
            return "non_field_errors"
    try:
        return str(loc)
    except Exception:
        return "non_field_errors"


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        grouped: dict = {}

        for err in exc.errors():
            # loc costuma ser algo como ["body", "password"]
            field = _extract_field_from_loc(err.get("loc", ["non_field_errors"]))
            # preferimos msg (mensagem original do pydantic/validator); fallback para str(err)
            message = err.get("msg") or err.get("type") or str(err)
            # # remove prefixo padrão do Pydantic
            if isinstance(message, str) and message.lower().startswith("value error,"):
                message = message.split(",", 1)[1].strip()
            
            grouped.setdefault(field, []).append(message)

        return JSONResponse(status_code=400, content={"errors": grouped})

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        Padroniza todas as HTTPExceptions para o mesmo formato:
        {"errors": { "<field>": ["<message>", ...] }}
        Não traduz nada: devolve as mensagens originais.
        """

        grouped: dict = {}

        detail = exc.detail

        # Se detail for um dict, tenta extrair field/message
        if isinstance(detail, dict):
            # field pode estar em 'field' ou 'loc'
            field = detail.get("field") or detail.get("loc") or "non_field_errors"
            # se loc for lista, extrai o último item
            if isinstance(field, (list, tuple)) and field:
                field = field[-1]
            # mensagem: procura chaves comuns
            message = detail.get("message") or detail.get("msg") or detail.get("detail") or str(detail)
            grouped.setdefault(str(field), []).append(message)

        # Se detail for uma lista (ex.: lista de erros), tenta extrair mensagens individuais
        elif isinstance(detail, (list, tuple)):
            for item in detail:
                # item pode ser dict (como pydantic.errors) ou string
                if isinstance(item, dict):
                    field = _extract_field_from_loc(item.get("loc", ["non_field_errors"]))
                    message = item.get("msg") or item.get("message") or str(item)
                    grouped.setdefault(field, []).append(message)
                else:
                    grouped.setdefault("non_field_errors", []).append(str(item))

        # Se detail for string ou outro tipo simples, devolve sob non_field_errors
        else:
            grouped.setdefault("non_field_errors", []).append(str(detail) if detail is not None else "Erro")

        # Retorna com o mesmo status_code da exceção
        return JSONResponse(status_code=exc.status_code, content={"errors": grouped})
