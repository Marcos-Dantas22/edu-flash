import pytest
from faker import Faker
from modules.users.models import User
from modules.users.utils import GenderEnum
from core.security import hash_password

fake = Faker()

@pytest.fixture
def fake_user(test_db):
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