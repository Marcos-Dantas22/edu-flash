from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

ERROR_MESSAGES_PT = {
    "string_too_short": "O campo deve ter pelo menos {min_length} caracteres.",
    "string_too_long": "O campo deve ter no máximo {max_length} caracteres.",
    "value_error.email": "O e-mail informado é inválido.",
    "missing": "Campo obrigatório.",
}


def translate_error(error: dict) -> str:
    error_type = error["type"]
    ctx = error.get("ctx", {})

    template = ERROR_MESSAGES_PT.get(error_type)

    # Caso não exista tradução, cai para uma mensagem padrão
    if not template:
        return "Valor inválido."

    try:
        return template.format(**ctx)
    except:
        return template


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):

        grouped = {}

        for err in exc.errors():
            field = err["loc"][-1]
            message = translate_error(err)

            grouped.setdefault(field, []).append(message)

        return JSONResponse(
            status_code=400,
            content={
                # "success": False,
                "errors": grouped
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        Formata exceções HTTP (ex.: 409 Conflict) para um JSON consistente.
        Para 409 retornamos um objeto `errors` em vez de usar o campo `detail`.
        """
        # para conflitos (409) queremos retornar como erros agrupados
        if exc.status_code == 409:
            # exc.detail pode ser string ou dict; prefer um formato estruturado {field, message}
            detail = exc.detail
            if isinstance(detail, dict):
                field = detail.get("field") or detail.get("loc") or "non_field_errors"
                # se loc for uma lista, pega o último item
                if isinstance(field, (list, tuple)) and len(field) > 0:
                    field = field[-1]
                message = detail.get("message") or detail.get("detail") or str(detail)
            else:
                field = "non_field_errors"
                message = str(detail) if detail is not None else "Conflict"

            return JSONResponse(status_code=409, content={"errors": {field: [message]}})

        # comportamento padrão para outras HTTPExceptions
        return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})
    
