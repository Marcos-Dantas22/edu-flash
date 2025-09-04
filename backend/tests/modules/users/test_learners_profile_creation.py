from faker import Faker
from passlib.hash import bcrypt
from modules.users.models import User, Teacher, Learner
from modules.users.utils import GenderEnum

fake = Faker()

def test_create_learner(test_db, fake_user, fake_teacher):
    teacher = fake_teacher
    user = fake_user

    learner = Learner(
        user_id=user.id,
        teacher_id=teacher.id,
        total_flash_hits=12,
        total_flash_errors=3,
        total_games_finished=6,
        total_group_memorized=2,
    )
    test_db.add(learner)
    test_db.commit()
    test_db.refresh(learner)

    db_learner = test_db.query(Learner).filter_by(id=learner.id).first()
    assert db_learner is not None
    assert db_learner.user_id == user.id
    assert db_learner.teacher_id == teacher.id
    assert db_learner.total_flash_hits == 12
    assert db_learner.total_flash_errors == 3
    assert db_learner.total_games_finished == 6
    assert db_learner.total_group_memorized == 2
    assert db_learner.is_active is True
    assert db_learner.created is not None
    assert db_learner.last_update is not None


def test_learner_relationship_with_teacher(test_db, fake_user, fake_teacher):
    teacher = fake_teacher
    user = fake_user

    learner = Learner(user_id=user.id, teacher_id=teacher.id)
    test_db.add(learner)
    test_db.commit()
    test_db.refresh(learner)

    # Testa navegação ORM Learner → Teacher
    assert learner.teacher is not None
    assert learner.teacher.id == teacher.id
    assert learner.teacher.learners[0] == learner  # Navegação Teacher → Learners


def test_learner_defaults(test_db, fake_user, fake_teacher):
    teacher = fake_teacher
    user = fake_user

    learner = Learner(user_id=user.id, teacher_id=teacher.id)
    test_db.add(learner)
    test_db.commit()
    test_db.refresh(learner)

    # Verifica valores padrão
    assert learner.total_flash_hits == 0
    assert learner.total_flash_errors == 0
    assert learner.total_games_finished == 0
    assert learner.total_group_memorized == 0
    assert learner.is_active is True
    assert learner.created is not None
    assert learner.last_update is not None
