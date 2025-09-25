import pytest
from modules.flashcards.models import FlashcardMultipleChoice
from modules.flashcards.utils import FlashcardTypes
from faker import Faker

fake = Faker()

@pytest.fixture
def fake_flashcard_multiple_choice(test_db):
    flashcard_multiple_choice= FlashcardMultipleChoice(
        flashcard_type=FlashcardTypes.MULTIPLE_CHOICE,
        question=fake.sentence(nb_words=6),
        answer1="A",
        answer2="B",
        answer3="C"
    )
    test_db.add(flashcard_multiple_choice)
    test_db.commit()
    test_db.refresh(flashcard_multiple_choice)
    return flashcard_multiple_choice
