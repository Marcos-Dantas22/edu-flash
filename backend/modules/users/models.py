from sqlalchemy import (
    Column, Integer, String, Boolean, Enum,
    ForeignKey, Date, DateTime
)
from sqlalchemy.orm import relationship
from core.database import Base
from modules.users.utils import GenderEnum
from datetime import datetime
from sqlalchemy.sql import func
from passlib.hash import bcrypt

class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, index=True)
    username = Column("usuario", String, unique=True, index=True)
    full_name = Column("nome completo", String, unique=True )
    email = Column("email", String, unique=True)
    password = Column("password", String, nullable=False)
    gender = Column("sexo", Enum(GenderEnum), nullable=False, default=GenderEnum.NONE)
    birth_date = Column("data de nascimento", Date)
    is_active = Column("é ativo?", Boolean, default=True)
    created = Column("criado em", DateTime, default=datetime.now())
    last_update = Column("ultima atualização", DateTime, server_default=func.now(), onupdate=func.now())

    # @property
    # def password(self):
    #     raise AttributeError("Password is write-only!")

    # @password.setter
    # def password(self, plain_password):
    #     self._password = bcrypt.hash(plain_password)

    def check_password(self, plain_password):
        return bcrypt.verify(plain_password, self.password)
    
    # def display_name(self):
    #     return self.name.title()

    # # método customizado
    # def greet(self):
    #     return f"Olá, {self.name}!"