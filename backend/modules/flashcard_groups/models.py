from sqlalchemy import (
    Column, Integer, String, Boolean, Enum,
    ForeignKey, Date, DateTime, Table
)
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
from sqlalchemy.sql import func
from modules.flashcard_groups.utils import LevelEnum, TypePermissionEnum

class GroupFlashCards(Base):
    __tablename__ = "group_flashcards"
    id = Column("id", Integer, primary_key=True, index=True)
    students = relationship(
        "Student",
        secondary="student_group_flashcards",
        back_populates="group_of_flashcards"
    )
    description = Column("descrição", String)
    next_interval_game = Column("prazo para próxima revisão", Date)
    percentage_memorized = Column("percentual memorizados?", Integer, default=0)
    is_active = Column("é ativo?", Boolean, default=True)
    created = Column("criado em", DateTime, default=datetime.now())
    last_update = Column("ultima atualização", DateTime, server_default=func.now(), onupdate=func.now())

    ##TODO: adicionar manytomany para flashcards


class GroupFlashCardsByTeacher(Base):
    __tablename__ = "group_flashcards_by_teacher"
    id = Column("id", Integer, primary_key=True, index=True)
    teachers = relationship(
        "Teacher",
        secondary="teacher_group_flashcards",
        back_populates="group_of_flashcards"
    )
    description = Column("descrição", String)
    level = Column("nivel de dificuldade", Enum(LevelEnum), nullable=False, default=LevelEnum.EASY)
    next_interval_game = Column("prazo para próxima revisão", Date)

    percentage_memorized = Column("percentual memorizados?", Integer, default=0)
    is_active = Column("é ativo?", Boolean, default=True)
    created = Column("criado em", DateTime, default=datetime.now())
    last_update = Column("ultima atualização", DateTime, server_default=func.now(), onupdate=func.now())

    ##TODO: adicionar manytomany para flashcards


class GroupFlashCardsProgress(Base):
    __tablename__ = "group_flashcards_progress"
    id = Column("id", Integer, primary_key=True, index=True)

    group_of_flashcards_id = Column("grupo de flashcards associado", Integer, ForeignKey('group_flashcards_by_teacher.id'), nullable=False)
    group_of_flashcards = relationship("GroupFlashCardsByTeacher")

    next_interval_game = Column("prazo para próxima revisão", Date)
    percentage_memorized = Column("percentual memorizados?", Integer, default=0)

    learner_id = Column("aprendiz", Integer, ForeignKey('learners.id'), nullable=False)
    learner = relationship("Learner")

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
permission_learners = Table(
    "permission_learners",
    Base.metadata,
    Column("learner_id", Integer, ForeignKey("learners.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id"))
)

class Permission(Base):
    __tablename__ = "permissions"
    id = Column("id", Integer, primary_key=True, index=True)

    type = Column("tipo de permissão", Enum(TypePermissionEnum), nullable=False)
   
    learners = relationship(
        "Learner",
        secondary=permission_learners,
        back_populates="permissions",  
    )

    date_limit = Column(
        "data limite de disponibilidade",
        Date,
        nullable=True 
    )
    
    group_of_flashcards_id = Column("grupo de flashcards associado", Integer, ForeignKey('group_flashcards_by_teacher.id'), nullable=False)
    group_of_flashcards = relationship("GroupFlashCardsByTeacher")

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
