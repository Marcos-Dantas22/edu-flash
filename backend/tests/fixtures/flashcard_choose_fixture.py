import pytest
from modules.flashcards.models import FlashcardChoose
from modules.flashcards.utils import FlashcardTypes
from faker import Faker

fake = Faker()

@pytest.fixture
def fake_flashcard_choose(test_db):
    flashcard_choose = FlashcardChoose(
        flashcard_type=FlashcardTypes.CHOOSE,
        base_text='Esta é uma frase de exemplo com a palavra-chave palavra.',
        keywords=["palavra"]
    )
    test_db.add(flashcard_choose)
    test_db.commit()
    test_db.refresh(flashcard_choose)
    return flashcard_choose
