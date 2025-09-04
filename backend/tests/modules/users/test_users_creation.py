from passlib.hash import bcrypt
from modules.users.models import User
from modules.users.utils import GenderEnum
import re
from faker import Faker

fake = Faker()

def test_create_user(test_db):
    # Gera dados fake
    username = fake.user_name()
    full_name = fake.name()
    email = fake.email()
    password = bcrypt.hash("senha123")
    gender = GenderEnum.MALE

    user = User(
        username=username,
        full_name=full_name,
        email=email,
        password=password, 
        gender=gender
    )
    test_db.add(user)
    test_db.commit()

    # Recupera do banco
    db_user = test_db.query(User).filter_by(username=username).first()
    assert db_user is not None
    assert db_user.username == username
    assert db_user.full_name == full_name
    assert db_user.gender == GenderEnum.MALE
    assert db_user.email == email
    # Verifica hash
    assert db_user.password != "senha123"
    assert bcrypt.verify("senha123", db_user.password)

def test_invalid_email_format():
    # Regex simples para validar email
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    valid_email = "teste@dominio.com"
    invalid_email = "teste@dominio"

    assert re.match(pattern, valid_email)
    assert not re.match(pattern, invalid_email)

def test_check_password(test_db):
    # Gera dados fake
    username = fake.user_name()
    full_name = fake.name()
    email = fake.email()
    password = bcrypt.hash("senha123")
    gender = GenderEnum.FEMALE

    user = User(
        username=username,
        full_name=full_name,
        email=email,
        password=password,
        gender=gender
    )
    test_db.add(user)
    test_db.commit()

    db_user = test_db.query(User).filter_by(username=username).first()
    assert db_user.check_password("senha123") is True
    assert db_user.check_password("senhaerrada") is False
