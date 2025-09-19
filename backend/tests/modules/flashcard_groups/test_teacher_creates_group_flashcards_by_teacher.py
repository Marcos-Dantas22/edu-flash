from modules.users.models import Teacher, User
from modules.flashcard_groups.models import GroupFlashCardsByTeacher
from modules.flashcard_groups.utils import LevelEnum
from faker import Faker

fake = Faker()

def test_teacher_creates_group_flashcards_by_teacher(test_db, fake_user):
    teacher = Teacher(
        user_id=fake_user.id,
        total_flash_hits=0,
        total_flash_errors=0,
        total_games_finished=0,
        total_group_memorized=0,
        is_active=True
    )
    test_db.add(teacher)
    test_db.commit()

    # Cria grupo de flashcards por professor
    description = fake.sentence(nb_words=4)
    next_interval_game = fake.date_between(start_date="today", end_date="+30d")
    percentage_memorized = fake.random_int(min=0, max=100)
    is_active = True
    level = LevelEnum.MEDIUM

    group = GroupFlashCardsByTeacher(
        description=description,
        next_interval_game=next_interval_game,
        percentage_memorized=percentage_memorized,
        is_active=is_active,
        level=level
    )
    test_db.add(group)
    test_db.commit()

    # Associa grupo ao professor
    teacher.group_of_flashcards.append(group)
    test_db.commit()

    db_teacher = test_db.query(Teacher).filter_by(id=teacher.id).first()
    assert db_teacher is not None
    assert len(db_teacher.group_of_flashcards) == 1
    assert group in db_teacher.group_of_flashcards

    db_group = test_db.query(GroupFlashCardsByTeacher).filter_by(id=group.id).first()
    assert db_teacher in db_group.teachers