from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from modules.users.models import User


class AuthService:
    @staticmethod
    def register_user(db: Session, data):
        # validações de unicidade
        if User.get_user_by_username(db, data.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"field": "username", "message": "username ja registrado"},
            )

        if User.get_user_by_email(db, data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"field": "email", "message": "email ja registrado"},
            )

        # password já validado pelo Pydantic schema (não vazio)
        # create_user fará o hash internamente
        return User.create_user(db=db, username=data.username, email=data.email, password=data.password)

    # @staticmethod
    # def login(db: Session, username: str, password: str):
    #     user = AuthRepository.get_user_by_username(db, username)

    #     if not user:
    #         return None

    #     if not verify_password(password, user.hashed_password):
    #         return None

    #     token = create_access_token({"sub": str(user.id)})
    #     return token
