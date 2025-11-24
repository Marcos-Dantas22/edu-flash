from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session

from core.database import get_db
from .schemas import UserCreate, UserResponse, LoginInput, LoginResponse
from .services import AuthService  
from .docs import (
    SIGNUP_SUMMARY,
    SIGNUP_DESCRIPTION,
    SIGNUP_TAGS,
    SIGNUP_BODY_EXAMPLE,
    SIGNUP_RESPONSES,
)

router = APIRouter()

@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=201,
    summary=SIGNUP_SUMMARY,
    description=SIGNUP_DESCRIPTION,
    tags=SIGNUP_TAGS,
    responses=SIGNUP_RESPONSES,
)
def register_user(
    data: UserCreate = Body(..., example=SIGNUP_BODY_EXAMPLE),
    db: Session = Depends(get_db),
):
    user = AuthService.register_user(db, data)
    return user


# @router.post("/login", response_model=LoginResponse)
# def login_user(body: LoginInput, db: Session = Depends(get_db)):
#     token = AuthService.login(db, body.username, body.password)

#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials"
#         )

#     return LoginResponse(access_token=token)
