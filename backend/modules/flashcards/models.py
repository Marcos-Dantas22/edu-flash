from sqlalchemy import (
    Column, Integer, String, Boolean, Enum,
    DateTime, JSON, ForeignKey
)
from core.database import Base
from datetime import datetime
from sqlalchemy.sql import func
from modules.flashcards.utils import FlashcardTypes
from sqlalchemy.orm import Session, validates

class Flashcard(Base):
    __tablename__ = "flashcards"
    id = Column("id", Integer, primary_key=True, index=True)
    flashcard_type = Column("tipo de flashcard", Enum(FlashcardTypes), nullable=False)
    is_active = Column("é ativo?", Boolean, default=True)
    created = Column("criado em", DateTime, default=datetime.now())
    last_update = Column("ultima atualização", DateTime, server_default=func.now(), onupdate=func.now())
    
    __mapper_args__ = {
        "polymorphic_identity": "flashcard",      
        "polymorphic_on": flashcard_type,        
    }

class FlashcardBasic(Flashcard):
    __tablename__ = "flashcard_basic"
    id = Column(Integer, ForeignKey("flashcards.id"), primary_key=True)
    front_side_text = Column("frente", String, nullable=False)
    back_side_text = Column("verso", String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": FlashcardTypes.BASIC,   
    }


class FlashcardChoose(Flashcard):
    __tablename__ = "flashcard_choose"
    id = Column(Integer, ForeignKey("flashcards.id"), primary_key=True)
    base_text = Column("texto base", String, nullable=False)
    keywords = Column("palavras-chave", JSON, nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": FlashcardTypes.CHOOSE,
    }

    @validates("keywords")
    def validate_keywords(self, key, keywords):
        for word in keywords:
            if word not in self.base_text:
                raise ValueError(f"A palavra-chave '{word}' não está presente em base_text")
        return keywords

class FlashcardMultipleChoice(Flashcard):
    __tablename__ = "flashcard_multiple_choice"
    id = Column(Integer, ForeignKey("flashcards.id"), primary_key=True)
    question = Column("pergunta", String, nullable=False)
    answer1 = Column("resposta 1", String, nullable=False)
    answer2 = Column("resposta 2", String, nullable=False)
    answer3 = Column("resposta 3", String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": FlashcardTypes.MULTIPLE_CHOICE,
    }