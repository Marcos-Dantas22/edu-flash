import pytest
from modules.users.models import Teacher

@pytest.fixture
def fake_teacher(test_db, fake_user):
    teacher = Teacher(user_id=fake_user.id)
    test_db.add(teacher)
    test_db.commit()
    test_db.refresh(teacher)
    return teacher
