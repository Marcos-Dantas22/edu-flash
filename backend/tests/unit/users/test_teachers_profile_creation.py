from faker import Faker
from passlib.hash import bcrypt
from modules.users.models import User, Teacher, Learner
from modules.users.utils import GenderEnum
from core.security import hash_password, verify_password

fake = Faker()


def create_fake_user(test_db):
    """Função auxiliar para criar um usuário válido."""
    user = User(
        username=fake.user_name(),
        full_name=fake.name(),
        email=fake.email(),
        hashed_password=hash_password("senha123"),
        gender=GenderEnum.MALE,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

def test_create_teacher(test_db, fake_user):
    user = fake_user

    teacher = Teacher(
        user_id=user.id,
        total_flash_hits=10,
        total_flash_errors=2,
        total_games_finished=5,
        total_group_memorized=3,
    )
    test_db.add(teacher)
    test_db.commit()
    test_db.refresh(teacher)

    db_teacher = test_db.query(Teacher).filter_by(id=teacher.id).first()
    assert db_teacher is not None
    assert db_teacher.user_id == user.id
    assert db_teacher.total_flash_hits == 10
    assert db_teacher.total_flash_errors == 2
    assert db_teacher.total_games_finished == 5
    assert db_teacher.total_group_memorized == 3
    assert db_teacher.is_active is True
    assert db_teacher.created is not None
    assert db_teacher.last_update is not None


def test_teacher_relationship_with_learners(test_db, fake_user):
    user = fake_user
    teacher = Teacher(user_id=user.id)
    test_db.add(teacher)
    test_db.commit()
    test_db.refresh(teacher)

    # Cria alguns learners associados a este teacher
    for _ in range(3):
        learner_user = create_fake_user(test_db)
        learner = Learner(user_id=learner_user.id, teacher=teacher)
        test_db.add(learner)

    test_db.commit()
    test_db.refresh(teacher)

    # Testa navegação Teacher → Learners
    assert len(teacher.learners) == 3
    for learner in teacher.learners:
        assert learner.teacher_id == teacher.id
        assert learner.teacher is teacher


def test_teacher_defaults(test_db, fake_user):
    user = fake_user

    teacher = Teacher(user_id=user.id)
    test_db.add(teacher)
    test_db.commit()
    test_db.refresh(teacher)

    # Verifica valores padrão
    assert teacher.total_flash_hits == 0
    assert teacher.total_flash_errors == 0
    assert teacher.total_games_finished == 0
    assert teacher.total_group_memorized == 0
    assert teacher.is_active is True
    assert teacher.created is not None
    assert teacher.last_update is not None
