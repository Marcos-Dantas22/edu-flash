from sqlalchemy import (
    Column, Integer, String, Boolean, Enum,
    ForeignKey, Date, DateTime, Table
)
from sqlalchemy.orm import relationship
from core.database import Base
from modules.users.utils import GenderEnum, LanguageEnum
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


# Tabela de associação
student_group_flashcards = Table(
    "student_group_flashcards",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("group_id", Integer, ForeignKey("group_flashcards.id"))
)
class Student(Base):
    __tablename__ = "students"

    id = Column("id", Integer, primary_key=True, index=True)
    user_id = Column("usuario", Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User")

    total_flash_hits = Column("total de flashcards acertados?", Integer, default=0)
    total_flash_errors = Column("total de flashcards errados?", Integer, default=0)
    total_games_finished = Column("total de jogos finalizados?", Integer, default=0)
    total_group_memorized = Column("total de grupos memorizados?", Integer, default=0)

    group_of_flashcards = relationship(
        "GroupFlashCards",
        secondary=student_group_flashcards,
        back_populates="students",
    )
    is_active = Column("é ativo?", Boolean, default=True)
    created = Column("criado em", DateTime, default=datetime.now())
    last_update = Column("ultima atualização", DateTime, server_default=func.now(), onupdate=func.now())

    # @property
    # def password(self):
    #     raise AttributeError("Password is write-only!")
    
    # def display_name(self):
    #     return self.name.title()

    # # método customizado
    # def greet(self):
    #     return f"Olá, {self.name}!"



# Tabela de associação
teacher_group_flashcards = Table(
    "teacher_group_flashcards",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id")),
    Column("group_id", Integer, ForeignKey("group_flashcards_by_teacher.id"))
)

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column("id", Integer, primary_key=True, index=True)
    user_id = Column("usuario", Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User")

    total_flash_hits = Column("total de flashcards acertados?", Integer, default=0)
    total_flash_errors = Column("total de flashcards errados?", Integer, default=0)
    total_games_finished = Column("total de jogos finalizados?", Integer, default=0)
    total_group_memorized = Column("total de grupos memorizados?", Integer, default=0)

    group_of_flashcards = relationship(
        "GroupFlashCardsByTeacher",
        secondary=teacher_group_flashcards,
        back_populates="teachers",
    )

    learners = relationship("Learner", back_populates="teacher")

    is_active = Column("é ativo?", Boolean, default=True)
    created = Column("criado em", DateTime, default=datetime.now())
    last_update = Column("ultima atualização", DateTime, server_default=func.now(), onupdate=func.now())

    # @property
    # def password(self):
    #     raise AttributeError("Password is write-only!")
    
    # def display_name(self):
    #     return self.name.title()

    # # método customizado
    # def greet(self):
    #     return f"Olá, {self.name}!"


class Learner(Base):
    __tablename__ = "learners"

    id = Column("id", Integer, primary_key=True, index=True)
    user_id = Column("usuario", Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User")

    total_flash_hits = Column("total de flashcards acertados?", Integer, default=0)
    total_flash_errors = Column("total de flashcards errados?", Integer, default=0)
    total_games_finished = Column("total de jogos finalizados?", Integer, default=0)
    total_group_memorized = Column("total de grupos memorizados?", Integer, default=0)

    ##TODO: adicionar manytomany para grupo de flashcards em progresso

    teacher_id = Column("professor", Integer, ForeignKey("teachers.id"), nullable=False)
    teacher = relationship("Teacher", back_populates="learners")

    is_active = Column("é ativo?", Boolean, default=True)
    created = Column("criado em", DateTime, default=datetime.now())
    last_update = Column("ultima atualização", DateTime, server_default=func.now(), onupdate=func.now())

    # @property
    # def password(self):
    #     raise AttributeError("Password is write-only!")
    
    # def display_name(self):
    #     return self.name.title()

    # # método customizado
    # def greet(self):
    #     return f"Olá, {self.name}!"

class UserConfig(Base):
    __tablename__ = 'usersconfig'
    id = Column("id", Integer, primary_key=True, index=True)
    dark_mode = Column("modo escuro ativo?", Boolean, default=False)
    language = Column("idioma", Enum(LanguageEnum), nullable=False, default=LanguageEnum.PORTUGUESE_BR)
    created = Column("criado em", DateTime, default=datetime.now())
    last_update = Column("ultima atualização", DateTime, server_default=func.now(), onupdate=func.now())

    # @property
    # def password(self):
    #     raise AttributeError("Password is write-only!")
    
    # def display_name(self):
    #     return self.name.title()

    # # método customizado
    # def greet(self):
    #     return f"Olá, {self.name}!"
