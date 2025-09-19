from sqlalchemy import (
    Column, Integer, String, Boolean, Enum,
    ForeignKey, Date, DateTime
)
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
from sqlalchemy.sql import func
from modules.flashcard_groups.utils import LevelEnum

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

    ##TODO: adicionar foreigh key para permissões de grupo de flashcards

    percentage_memorized = Column("percentual memorizados?", Integer, default=0)
    is_active = Column("é ativo?", Boolean, default=True)
    created = Column("criado em", DateTime, default=datetime.now())
    last_update = Column("ultima atualização", DateTime, server_default=func.now(), onupdate=func.now())

    ##TODO: adicionar manytomany para flashcards