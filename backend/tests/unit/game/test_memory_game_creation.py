from modules.game.models import MemoryGame
from faker import Faker
import pytest

fake = Faker()

def test_create_memory_game_by_student(test_db, fake_user, fake_group_of_flashcard):
    count_hits = fake.random_int(min=0, max=100)
    count_mistakes = fake.random_int(min=0, max=100)

    memory_game = MemoryGame(
        user=fake_user,
        group_type="student",
        group_id=fake_group_of_flashcard.id,
        count_hits=count_hits,
        count_mistakes=count_mistakes,
    )
    test_db.add(memory_game)
    test_db.commit()

    db_memory_game = test_db.query(MemoryGame).filter_by(group_type='student', group_id=fake_group_of_flashcard.id).first()
    assert db_memory_game is not None
    assert db_memory_game.count_hits == count_hits
    assert db_memory_game.count_mistakes == count_mistakes
    assert db_memory_game.is_active is True


def test_create_memory_game_by_teacher(test_db, fake_user, fake_group_flashcard_by_teacher):
    count_hits = fake.random_int(min=0, max=100)
    count_mistakes = fake.random_int(min=0, max=100)

    memory_game = MemoryGame(
        user=fake_user,
        group_type="teacher",
        group_id=fake_group_flashcard_by_teacher.id,
        count_hits=count_hits,
        count_mistakes=count_mistakes,
    )
    test_db.add(memory_game)
    test_db.commit()

    db_memory_game = test_db.query(MemoryGame).filter_by(group_type='teacher', group_id=fake_group_flashcard_by_teacher.id).first()
    assert db_memory_game is not None
    assert db_memory_game.count_hits == count_hits
    assert db_memory_game.count_mistakes == count_mistakes
    assert db_memory_game.is_active is True

def test_memory_game_invalid_group_type_raises(test_db, fake_user):
    with pytest.raises(ValueError) as excinfo:
        memory_game = MemoryGame(
            user=fake_user,
            group_type="invalid_type",  # inválido
            group_id=999
        )
        test_db.add(memory_game)
        test_db.commit()

    assert "não faz parte das opções disponiveís" in str(excinfo.value)


def test_memory_game_get_group_student(test_db, fake_user, fake_group_of_flashcard):
    memory_game = MemoryGame(
        user=fake_user,
        group_type="student",
        group_id=fake_group_of_flashcard.id,
    )
    test_db.add(memory_game)
    test_db.commit()

    db_game = test_db.query(MemoryGame).first()
    group = db_game.get_group(test_db)

    assert group is not None
    assert group.id == fake_group_of_flashcard.id
    assert group.description == fake_group_of_flashcard.description

def test_memory_game_get_group_teacher(test_db, fake_user, fake_group_flashcard_by_teacher):
    memory_game = MemoryGame(
        user=fake_user,
        group_type="teacher",
        group_id=fake_group_flashcard_by_teacher.id,
    )
    test_db.add(memory_game)
    test_db.commit()

    db_game = test_db.query(MemoryGame).first()
    group = db_game.get_group(test_db)

    assert group is not None
    assert group.id == fake_group_flashcard_by_teacher.id
    assert group.description == fake_group_flashcard_by_teacher.description