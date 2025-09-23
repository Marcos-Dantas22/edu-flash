import pytest
from modules.flashcard_groups.models import GroupFlashCardsByTeacher, LevelEnum
from faker import Faker

fake = Faker()

@pytest.fixture
def fake_group_flashcard_by_teacher(test_db):
    group = GroupFlashCardsByTeacher(
        description=fake.sentence(nb_words=4),
        next_interval_game=fake.date_between(start_date="today", end_date="+30d"),
        level=LevelEnum.EASY,
    )
    test_db.add(group)
    test_db.commit()
    test_db.refresh(group)
    return group
