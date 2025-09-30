import pytest
from modules.flashcard_groups.models import GroupFlashCards
from faker import Faker

fake = Faker()

@pytest.fixture
def fake_group_of_flashcard(test_db):
    group = GroupFlashCards(
        description=fake.sentence(nb_words=4),
        next_interval_game=fake.date_between(start_date="today", end_date="+30d"),
        percentage_memorized = fake.random_int(min=0, max=100),
        is_active = True
    )
    test_db.add(group)
    test_db.commit()
    test_db.refresh(group)
    return group
