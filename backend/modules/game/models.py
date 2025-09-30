from sqlalchemy import (
    Column, Integer, String, Boolean, Enum,
    ForeignKey, Date, DateTime, Table
)
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, validates
from modules.flashcard_groups.models import GroupFlashCards, GroupFlashCardsByTeacher

class MemoryGame(Base):
    __tablename__ = "memory_game"

    id = Column("id", Integer, primary_key=True, index=True)
    user_id = Column("usuario", Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User")

    # guarda o tipo de grupo (teacher or student) e o id do grupo
    group_type = Column(String, nullable=False)  
    group_id = Column(Integer, nullable=False)   

    count_hits = Column("total de flashcards acertados?", Integer, default=0)
    count_mistakes = Column("total de flashcards errados?", Integer, default=0)

    is_active = Column("é ativo?", Boolean, default=True)
    created = Column("criado em", DateTime, default=datetime.now())
    last_update = Column("ultima atualização", DateTime, server_default=func.now(), onupdate=func.now())
    
    @validates("group_type")
    def validate_group_type(self, key, group_type):
        if group_type not in ['student', 'teacher']:
            raise ValueError(f"O tipo de grupo '{group_type}' não faz parte das opções disponiveís")
        return group_type
    
    def get_group(self, session: Session):
        if self.group_type == "student":
            return session.get(GroupFlashCards, self.group_id)
        elif self.group_type == "teacher":
            return session.get(GroupFlashCardsByTeacher, self.group_id)
        return None