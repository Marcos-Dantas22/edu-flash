from modules.flashcards.models import FlashcardChoose
from modules.flashcards.utils import FlashcardTypes
import pytest

from faker import Faker

fake = Faker()

def test_create_flashcard_choose_valid(test_db):
    base_text = "Python é uma linguagem poderosa e flexível"
    keywords = ["Python", "poderosa"]
    is_active = True

    flashcard = FlashcardChoose(
        flashcard_type=FlashcardTypes.CHOOSE,
        base_text=base_text,
        keywords=keywords,
        is_active=is_active
    )
    test_db.add(flashcard)
    test_db.commit()

    db_flashcard = test_db.query(FlashcardChoose).filter_by(base_text=base_text).first()
    assert db_flashcard is not None
    assert db_flashcard.base_text == base_text
    assert db_flashcard.keywords == keywords
    assert db_flashcard.is_active is True

def test_create_flashcard_choose_invalid_keyword(test_db):
    base_text = "Python é incrível"
    keywords = ["Java"]  

    with pytest.raises(ValueError) as excinfo:
        flashcard = FlashcardChoose(
            flashcard_type=FlashcardTypes.CHOOSE,
            base_text=base_text,
            keywords=keywords
        )
        test_db.add(flashcard)
        test_db.commit()

    assert "não está presente em base_text" in str(excinfo.value)

def test_default_values_flashcard_choose(test_db):
    base_text = "FastAPI é escrito em Python"
    keywords = ["Python"]

    flashcard = FlashcardChoose(
        flashcard_type=FlashcardTypes.CHOOSE,
        base_text=base_text,
        keywords=keywords
    )
    test_db.add(flashcard)
    test_db.commit()

    db_flashcard = test_db.query(FlashcardChoose).filter_by(base_text=base_text).first()
    assert db_flashcard is not None
    assert db_flashcard.is_active is True
