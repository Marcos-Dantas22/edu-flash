import pytest
from modules.users.models import Learner

@pytest.fixture
def fake_learner(test_db, fake_user, fake_teacher):
    learner = Learner(user_id=fake_user.id, teacher_id=fake_teacher.id)
    test_db.add(learner)
    test_db.commit()
    test_db.refresh(learner)
    return learner
