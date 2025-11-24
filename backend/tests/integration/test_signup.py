import pytest
from main import app
from core.config import settings
from modules.users.models import User

@pytest.mark.integration
def test_signup_success(client, test_db):

    payload = {
        "username": "integ_user",
        "email": "integ_user@example.com",
        "birth_date": "1990-01-01",
        "password": "Aa1!passw"
    }

    headers = {"X-API-Key": settings.API_KEY}
    resp = client.post("/api/v1/auth/signup", json=payload, headers=headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]

    # also ensure user present in DB
    db_user = test_db.query(User).filter_by(username=payload["username"]).first()
    assert db_user is not None

    app.dependency_overrides.clear()

@pytest.mark.integration
def test_signup_duplicate_username_returns_error(client, test_db):
    # create existing user directly in DB
    existing = User.create_user(
        db=test_db,
        username="dup_user",
        email="dup@example.com",
        birth_date="1990-01-01",
        password="Aa1!passw"
    )

    payload = {
        "username": "dup_user",
        "email": "newemail@example.com",
        "birth_date": "1991-02-02",
        "password": "Aa1!passw"
    }

    headers = {"X-API-Key": settings.API_KEY}
    resp = client.post("/api/v1/auth/signup", json=payload, headers=headers)
    # service raises HTTPException with status 422 for duplicate
    assert resp.status_code == 422
    body = resp.json()
    # our handler returns the detail under the "message" key for non-409 HTTPExceptions
    assert "errors" in body
    errors = body["errors"]
    assert isinstance(errors, dict)
    assert "username" in errors
    assert isinstance(errors["username"], list)
    assert "username ja registrado" in errors["username"]

    app.dependency_overrides.clear()


@pytest.mark.integration
@pytest.mark.parametrize(
    "field,value",
    [
        ("username", ""),
        ("username", None),
        ("username", "has space"),
        ("username", 123),

        ("email", ""),
        ("email", None),
        ("email", "bad email@com"),
        ("email", ["not", "an", "email"]),

        ("birth_date", ""),
        ("birth_date", None),
        ("birth_date", "1990 01 01"),
        ("birth_date", 19900101),

        ("password", ""),
        ("password", None),
        ("password", "Short1!"),
        ("password", 12345678),
        ("password", "has space A1!"),
    ],
)
def test_signup_field_invalid_returns_400(client, test_db, field, value):
    # base valid payload
    payload = {
        "username": "valid_user",
        "email": "valid_user@example.com",
        "birth_date": "1990-01-01",
        "password": "Aa1!passw"
    }

    payload[field] = value
    headers = {"X-API-Key": settings.API_KEY}
    resp = client.post("/api/v1/auth/signup", json=payload, headers=headers)

    assert resp.status_code == 400
    body = resp.json()
    assert "errors" in body
    errors = body["errors"]
    # the validator should report an error for the field
    assert field in errors
    assert isinstance(errors[field], list)


@pytest.mark.integration
def test_signup_missing_api_key_returns_401(client, test_db):
    payload = {
        "username": "valid_user2",
        "email": "valid_user2@example.com",
        "birth_date": "1990-01-01",
        "password": "Aa1!passw"
    }

    # do not send API key header
    resp = client.post("/api/v1/auth/signup", json=payload)
    assert resp.status_code == 401
    body = resp.json()
    assert "errors" in body
    errors = body["errors"]
    assert isinstance(errors, dict)
    assert "api_key" in errors
    assert isinstance(errors["api_key"], list)
    assert "API Key inválida ou ausente" in errors["api_key"]