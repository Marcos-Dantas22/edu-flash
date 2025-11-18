from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from .schemas import UserCreate, UserResponse, LoginInput, LoginResponse
from .services import AuthService   

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
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
