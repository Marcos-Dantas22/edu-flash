from faker import Faker
from modules.flashcard_groups.models import GroupFlashCardsByTeacher, GroupFlashCardsProgress, LevelEnum
from modules.users.models import Learner
from datetime import date

fake = Faker()

def test_create_group_flashcards_progress(
    test_db, fake_group_flashcard_by_teacher, fake_learner
):
    group = fake_group_flashcard_by_teacher
    learner = fake_learner

    next_interval_game = fake.date_between(start_date="today", end_date="+30d")
    percentage_memorized = fake.random_int(min=0, max=100)

    progress = GroupFlashCardsProgress(
        group_of_flashcards_id=group.id,
        next_interval_game=next_interval_game,
        percentage_memorized=percentage_memorized,
        learner_id=learner.id,
        is_active=True,
    )
    test_db.add(progress)
    test_db.commit()

    db_progress = test_db.query(GroupFlashCardsProgress).filter_by(id=progress.id).first()
    assert db_progress is not None
    assert db_progress.group_of_flashcards_id == group.id
    assert db_progress.learner_id == learner.id
    assert db_progress.next_interval_game == next_interval_game
    assert db_progress.percentage_memorized == percentage_memorized
    assert db_progress.is_active is True


def test_default_values_group_flashcards_progress(
    test_db, fake_group_flashcard_by_teacher, fake_learner
):
    group = fake_group_flashcard_by_teacher
    learner = fake_learner

    progress = GroupFlashCardsProgress(
        group_of_flashcards_id=group.id,
        learner_id=learner.id,
    )
    test_db.add(progress)
    test_db.commit()

    db_progress = test_db.query(GroupFlashCardsProgress).filter_by(id=progress.id).first()
    assert db_progress is not None
    assert db_progress.percentage_memorized == 0
    assert db_progress.is_active is True
    assert isinstance(db_progress.created, date)
    assert db_progress.last_update is not None
