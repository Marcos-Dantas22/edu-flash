from modules.users.models import Student, User
from modules.flashcard_groups.models import GroupFlashCards
from faker import Faker
from datetime import date

fake = Faker()

def test_student_group_of_flashcards_interaction(test_db, fake_user):
    student = Student(
        user_id=fake_user.id,
        total_flash_hits=0,
        total_flash_errors=0,
        total_games_finished=0,
        total_group_memorized=0,
        is_active=True
    )
    test_db.add(student)
    test_db.commit()

    # Cria grupos de flashcards
    group1 = GroupFlashCards(
        description=fake.sentence(nb_words=4),
        next_interval_game=fake.date_between(start_date="today", end_date="+30d"),
        percentage_memorized=20,
        is_active=True
    )
    group2 = GroupFlashCards(
        description=fake.sentence(nb_words=4),
        next_interval_game=fake.date_between(start_date="today", end_date="+30d"),
        percentage_memorized=80,
        is_active=True
    )
    test_db.add(group1)
    test_db.add(group2)
    test_db.commit()

    # Associa os grupos ao estudante
    student.group_of_flashcards.append(group1)
    student.group_of_flashcards.append(group2)
    test_db.commit()

    # Testa se os grupos estão associados ao estudante
    db_student = test_db.query(Student).filter_by(id=student.id).first()
    assert db_student is not None
    assert len(db_student.group_of_flashcards) == 2
    assert group1 in db_student.group_of_flashcards
    assert group2 in db_student.group_of_flashcards

    # Testa se o estudante aparece nos grupos
    db_group1 = test_db.query(GroupFlashCards).filter_by(id=group1.id).first()
    db_group2 = test_db.query(GroupFlashCards).filter_by(id=group2.id).first()
    assert db_student in db_group1.students
    assert db_student in db_group2.students