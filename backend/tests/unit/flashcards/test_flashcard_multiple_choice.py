from modules.flashcards.models import FlashcardMultipleChoice
from modules.flashcards.utils import FlashcardTypes
from faker import Faker

fake = Faker()

def test_create_flashcard_multiple_choice(test_db):
    question = fake.sentence(nb_words=8)
    answer1 = fake.word()
    answer2 = fake.word()
    answer3 = fake.word()
    is_active = True

    flashcard = FlashcardMultipleChoice(
        flashcard_type=FlashcardTypes.MULTIPLE_CHOICE,
        question=question,
        answer1=answer1,
        answer2=answer2,
        answer3=answer3,
        is_active=is_active
    )
    test_db.add(flashcard)
    test_db.commit()

    db_flashcard = test_db.query(FlashcardMultipleChoice).filter_by(question=question).first()
    assert db_flashcard is not None
    assert db_flashcard.question == question
    assert db_flashcard.answer1 == answer1
    assert db_flashcard.answer2 == answer2
    assert db_flashcard.answer3 == answer3
    assert db_flashcard.is_active is True

def test_default_values_flashcard_multiple_choice(test_db):
    question = fake.sentence(nb_words=8)
    answer1 = fake.word()
    answer2 = fake.word()
    answer3 = fake.word()

    flashcard = FlashcardMultipleChoice(
        flashcard_type=FlashcardTypes.MULTIPLE_CHOICE,
        question=question,
        answer1=answer1,
        answer2=answer2,
        answer3=answer3
    )
    test_db.add(flashcard)
    test_db.commit()

    db_flashcard = test_db.query(FlashcardMultipleChoice).filter_by(question=question).first()
    assert db_flashcard is not None
    assert db_flashcard.is_active is True
