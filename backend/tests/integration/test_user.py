from backend.main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies
import random
import string
from passlib.context import CryptContext


client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
URL_USER = "/users"


def test_read_user_unit():
    remove_dependencies()

    value = ''.join(random.choice(string.ascii_letters) for _ in range(15))
    password = pwd_context.hash(value)

    response = client.post(
        URL_USER,
        json={
            "username": value,
            "email": f"{value}@email.com",
            "password": password,
            "passwordConfirmation": password

        }
    )

    user_id = response.json().get("data", {}).get("id", None)
    response = client.get(f"{URL_USER}/{user_id}/")
    assert response.status_code == 200

    resume_dependencies()


def test_read_users():
    remove_dependencies()

    response = client.get(
        URL_USER,
    )
    assert response.status_code == 200

    resume_dependencies()


def test_create_user():
    value = ''.join(random.choice(string.ascii_letters) for _ in range(15))
    password = pwd_context.hash(value)

    response = client.post(
        URL_USER,
        json={
            "username": value,
            "email": f"{value}@email.com",
            "password": password,
            "passwordConfirmation": password

        }
    )
    assert response.status_code == 201
