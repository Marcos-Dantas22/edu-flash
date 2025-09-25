from modules.flashcards.models import FlashcardBasic
from modules.flashcards.utils import FlashcardTypes
from faker import Faker

fake = Faker()

def test_create_flashcard_basic(test_db):
    front_text = fake.sentence(nb_words=6)
    back_text = fake.sentence(nb_words=10)

    flashcard = FlashcardBasic(
        flashcard_type=FlashcardTypes.BASIC,
        front_side_text=front_text,
        back_side_text=back_text,
        is_active=True
    )
    test_db.add(flashcard)
    test_db.commit()

    db_flashcard = test_db.query(FlashcardBasic).filter_by(front_side_text=front_text).first()
    assert db_flashcard is not None
    assert db_flashcard.front_side_text == front_text
    assert db_flashcard.back_side_text == back_text
    assert db_flashcard.is_active is True

def test_default_values_flashcard_basic(test_db):
    front_text = fake.sentence(nb_words=6)
    back_text = fake.sentence(nb_words=10)

    flashcard = FlashcardBasic(
        flashcard_type=FlashcardTypes.BASIC,
        front_side_text=front_text,
        back_side_text=back_text
    )
    test_db.add(flashcard)
    test_db.commit()

    db_flashcard = test_db.query(FlashcardBasic).filter_by(front_side_text=front_text).first()
    assert db_flashcard is not None
    assert db_flashcard.is_active is True
