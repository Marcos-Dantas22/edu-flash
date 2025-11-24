"""OpenAPI docs metadata for auth endpoints.

Keeping documentation metadata in a separate module keeps routes file small and
improves readability.
"""

SIGNUP_SUMMARY = "Criar conta (signup)"

SIGNUP_DESCRIPTION = (
    "Cria um novo usuário. Valida os campos (username, email, birth_date, password) "
    "e retorna os dados do usuário sem a senha. Requer header X-API-Key."
)

SIGNUP_TAGS = ["auth"]

SIGNUP_BODY_EXAMPLE = {
    "username": "joaosilva",
    "email": "joao@example.com",
    "birth_date": "1990-01-01",
    "password": "Aa1!passw",
}

SIGNUP_RESPONSES = {
    201: {"description": "Usuário criado com sucesso"},
    400: {
        "description": "Dados inválidos (validação)",
        "content": {"application/json": {"example": {"errors": {"username": ["username não pode ser vazio"]}}}},
    },
    401: {
        "description": "API Key ausente ou inválida",
        "content": {"application/json": {"example": {"errors": {"api_key": ["API Key inválida ou ausente"]}}}},
    },
    422: {
        "description": "Conflito - username/email já cadastrado",
        "content": {"application/json": {"example": {"errors": {"username": ["username ja registrado"]}}}},
    },
}
