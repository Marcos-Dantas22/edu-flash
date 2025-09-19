from modules.flashcard_groups.models import GroupFlashCards
from faker import Faker

fake = Faker()

def test_create_group_flashcards(test_db):
    description = fake.sentence(nb_words=4)
    next_interval_game = fake.date_between(start_date="today", end_date="+30d")
    percentage_memorized = fake.random_int(min=0, max=100)
    is_active = True

    group = GroupFlashCards(
        description=description,
        next_interval_game=next_interval_game,
        percentage_memorized=percentage_memorized,
        is_active=is_active
    )
    test_db.add(group)
    test_db.commit()

    db_group = test_db.query(GroupFlashCards).filter_by(description=description).first()
    assert db_group is not None
    assert db_group.description == description
    assert db_group.next_interval_game == next_interval_game
    assert db_group.percentage_memorized == percentage_memorized
    assert db_group.is_active is True

def test_default_values_group_flashcards(test_db):
    description = fake.sentence(nb_words=4)
    next_interval_game = fake.date_between(start_date="today", end_date="+30d")

    group = GroupFlashCards(
        description=description,
        next_interval_game=next_interval_game
    )
    test_db.add(group)
    test_db.commit()

    db_group = test_db.query(GroupFlashCards).filter_by(description=description).first()
    assert db_group is not None
    assert db_group.percentage_memorized == 0
    assert db_group.is_active is True