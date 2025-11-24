from datetime import datetime
from faker import Faker
from modules.flashcard_groups.models import Permission
from modules.flashcard_groups.utils import TypePermissionEnum

fake = Faker()

def test_create_permission(test_db, fake_group_flashcard_by_teacher, fake_learner):
    group = fake_group_flashcard_by_teacher
    learner = fake_learner

    date_limit = fake.date_between(start_date="today", end_date="+30d")

    permission = Permission(
        type=TypePermissionEnum.GROUP_PUBLIC,
        group_of_flashcards_id=group.id,
        date_limit=date_limit,
        is_active=True,
    )
    permission.learners.append(learner)

    test_db.add(permission)
    test_db.commit()

    db_permission = test_db.query(Permission).filter_by(id=permission.id).first()
    assert db_permission is not None
    assert db_permission.type == TypePermissionEnum.GROUP_PUBLIC
    assert db_permission.group_of_flashcards_id == group.id
    assert db_permission.date_limit == date_limit
    assert db_permission.is_active is True
    assert learner in db_permission.learners


def test_default_values_permission(test_db, fake_group_flashcard_by_teacher):
    group = fake_group_flashcard_by_teacher

    permission = Permission(
        type=TypePermissionEnum.GROUP_PRIVATE,
        group_of_flashcards_id=group.id,
    )
    test_db.add(permission)
    test_db.commit()

    db_permission = test_db.query(Permission).filter_by(id=permission.id).first()
    assert db_permission is not None
    assert db_permission.is_active is True
    assert isinstance(db_permission.created, datetime)
    assert db_permission.last_update is not None
    assert db_permission.date_limit is None


def test_permission_many_to_many_with_learners(
    test_db, fake_group_flashcard_by_teacher, fake_learner
):
    group = fake_group_flashcard_by_teacher
    learner = fake_learner

    permission = Permission(
        type=TypePermissionEnum.GROUP_PRIVATE,
        group_of_flashcards_id=group.id,
    )
    permission.learners.append(learner)

    test_db.add(permission)
    test_db.commit()

    db_permission = test_db.query(Permission).filter_by(id=permission.id).first()
    assert db_permission is not None
    assert len(db_permission.learners) == 1
    assert db_permission.learners[0].id == learner.id

    # também garantir o back_populates
    assert len(learner.permissions) == 1
    assert learner.permissions[0].id == permission.id
