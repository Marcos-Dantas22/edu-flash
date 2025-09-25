import pytest
from modules.flashcards.models import FlashcardBasic
from modules.flashcards.utils import FlashcardTypes
from faker import Faker

fake = Faker()

@pytest.fixture
def fake_flashcard_basic(test_db):
    flashcard_basic = FlashcardBasic(
        flashcard_type=FlashcardTypes.BASIC,
        front_side_text=fake.sentence(nb_words=5),
        back_side_text=fake.sentence(nb_words=10)
    )
    test_db.add(flashcard_basic)
    test_db.commit()
    test_db.refresh(flashcard_basic)
    return flashcard_basic
