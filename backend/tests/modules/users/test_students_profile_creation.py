from modules.users.models import User, Student
from modules.users.utils import GenderEnum
from passlib.hash import bcrypt
from faker import Faker

fake = Faker()


def create_fake_user(test_db):
    """Função auxiliar para criar um usuário válido."""
    user = User(
        username=fake.user_name(),
        full_name=fake.name(),
        email=fake.email(),
        password=bcrypt.hash("senha123"),
        gender=GenderEnum.MALE,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


def test_create_student(test_db, fake_user):
    user = fake_user

    student = Student(
        user_id=user.id,
        total_flash_hits=10,
        total_flash_errors=2,
        total_games_finished=5,
        total_group_memorized=3,
    )
    test_db.add(student)
    test_db.commit()

    db_student = test_db.query(Student).filter_by(user_id=user.id).first()
    assert db_student is not None
    assert db_student.user_id == user.id
    assert db_student.total_flash_hits == 10
    assert db_student.total_flash_errors == 2
    assert db_student.total_games_finished == 5
    assert db_student.total_group_memorized == 3
    assert db_student.is_active is True


def test_student_relationship_with_user(test_db, fake_user):
    user = fake_user

    student = Student(user_id=user.id)
    test_db.add(student)
    test_db.commit()
    test_db.refresh(student)

    # Testa navegação ORM Student → User
    assert student.user is not None
    assert student.user.id == user.id
    assert student.user.username == user.username


def test_student_defaults(test_db, fake_user):
    user = fake_user

    student = Student(user_id=user.id)
    test_db.add(student)
    test_db.commit()
    test_db.refresh(student)

    # Verifica se os valores padrão foram aplicados
    assert student.total_flash_hits == 0
    assert student.total_flash_errors == 0
    assert student.total_games_finished == 0
    assert student.total_group_memorized == 0
    assert student.is_active is True
    assert student.created is not None
    assert student.last_update is not None
