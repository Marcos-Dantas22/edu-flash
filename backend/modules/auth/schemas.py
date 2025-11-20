from pydantic import BaseModel, EmailStr, Field, validator
from typing import Any, Optional
import re

class UserCreate(BaseModel):
    username: Optional[Any] = None
    email: Optional[Any] = None
    birth_date: Optional[Any] = None
    password: Optional[Any] = None

    @validator("username")
    def validate_username(cls, v):
        if v is None:
            raise ValueError("username não pode ser nulo")

        if not isinstance(v, str):
            raise ValueError("username deve ser do tipo string")

        v = v.strip()
        if not v:
            raise ValueError("username não pode ser vazio")

        if " " in v:
            raise ValueError("username não pode conter espaços")

        if len(v) < 3 or len(v) > 50:
            raise ValueError("username deve ter entre 3 e 50 caracteres")

        return v

    @validator("email")
    def validate_email(cls, v):
        if v is None:
            raise ValueError("email não pode ser nulo")
        
        if not isinstance(v, str):
            raise ValueError("email deve ser do tipo string")

        v = v.strip()
        if not v:
            raise ValueError("email não pode ser vazio")

        if " " in v:
            raise ValueError("email não pode conter espaços")

        if "@" not in v or v.startswith("@") or v.endswith("@"):
            raise ValueError("email inválido")

        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_regex, v):
            raise ValueError("email inválido")
        
        return v

    @validator("birth_date")
    def validate_birth_date(cls, v):
        if v is None:
            raise ValueError("birth_date não pode ser nulo")

        if not isinstance(v, str):
            raise ValueError("birth_date deve ser do tipo string")

        v = v.strip()
        if not v:
            raise ValueError("birth_date não pode ser vazio")

        if " " in v:
            raise ValueError("birth_date não pode conter espaços")

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            raise ValueError("birth_date deve estar no formato YYYY-MM-DD")

        return v

    @validator("password")
    def validate_password(cls, v):
        if v is None:
            raise ValueError("password não pode ser nulo")
        
        if not isinstance(v, str):
            raise ValueError("password deve ser do tipo string")

        if not v.strip():
            raise ValueError("password não pode ser vazio")

        if " " in v:
            raise ValueError("password não pode conter espaços")

        if len(v) < 8:
            raise ValueError("password deve ter pelo menos 8 caracteres")

        if not re.search(r"[A-Z]", v):
            raise ValueError("password deve conter pelo menos uma letra maiúscula")

        if not re.search(r"[a-z]", v):
            raise ValueError("password deve conter pelo menos uma letra minúscula")

        if not re.search(r"[0-9]", v):
            raise ValueError("password deve conter pelo menos um número")

        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("password deve conter pelo menos um caractere especial")

        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
