import pytest
from faker import Faker
from passlib.hash import bcrypt
from modules.users.models import User
from modules.users.utils import GenderEnum

fake = Faker()

@pytest.fixture
def fake_user(test_db):
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