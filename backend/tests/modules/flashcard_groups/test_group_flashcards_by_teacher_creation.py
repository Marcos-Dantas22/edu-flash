from modules.flashcard_groups.models import GroupFlashCardsByTeacher
from modules.flashcard_groups.utils import LevelEnum
from faker import Faker

fake = Faker()

def test_create_group_flashcards_by_teacher(test_db):
    description = fake.sentence(nb_words=4)
    next_interval_game = fake.date_between(start_date="today", end_date="+30d")
    percentage_memorized = fake.random_int(min=0, max=100)
    is_active = True
    level = LevelEnum.EASY

    group = GroupFlashCardsByTeacher(
        description=description,
        next_interval_game=next_interval_game,
        percentage_memorized=percentage_memorized,
        is_active=is_active,
        level=level
    )
    test_db.add(group)
    test_db.commit()

    db_group = test_db.query(GroupFlashCardsByTeacher).filter_by(description=description).first()
    assert db_group is not None
    assert db_group.description == description
    assert db_group.next_interval_game == next_interval_game
    assert db_group.percentage_memorized == percentage_memorized
    assert db_group.is_active is True
    assert db_group.level == LevelEnum.EASY

def test_default_values_group_flashcards_by_teacher(test_db):
    description = fake.sentence(nb_words=4)
    next_interval_game = fake.date_between(start_date="today", end_date="+30d")

    group = GroupFlashCardsByTeacher(
        description=description,
        next_interval_game=next_interval_game
    )
    test_db.add(group)
    test_db.commit()

    db_group = test_db.query(GroupFlashCardsByTeacher).filter_by(description=description).first()
    assert db_group is not None
    assert db_group.percentage_memorized == 0
    assert db_group.is_active is True
    assert db_group.level == LevelEnum.EASY

def test_group_flashcards_by_teacher_many_to_many(test_db, fake_flashcard_basic, fake_flashcard_choose, fake_flashcard_multiple_choice):
    group = GroupFlashCardsByTeacher(
        description=fake.sentence(nb_words=4),
        next_interval_game=fake.date_between(start_date="today", end_date="+30d"),
        level=LevelEnum.MEDIUM,
        flashcards=[fake_flashcard_basic, fake_flashcard_choose, fake_flashcard_multiple_choice]
    )
    test_db.add(group)
    test_db.commit()

    db_group = test_db.query(GroupFlashCardsByTeacher).filter_by(id=group.id).first()
    assert db_group is not None
    assert len(db_group.flashcards) == 3
    types_in_group = {type(f).__name__ for f in db_group.flashcards}
    assert "FlashcardBasic" in types_in_group
    assert "FlashcardChoose" in types_in_group
    assert "FlashcardMultipleChoice" in types_in_group