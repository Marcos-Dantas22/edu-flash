from pydantic import BaseModel, EmailStr, Field, validator


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=1)

    @validator("username")
    def username_no_spaces(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("username não pode ser vazio")
        if " " in v:
            raise ValueError("username não pode conter espaços")
        return v

    @validator("password")
    def password_not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("password não pode ser vazio")
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
