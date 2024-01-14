from backend.main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies
from passlib.context import CryptContext
import os
import base64

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
URL_USER = "/users"


def test_read_user_unit():
    remove_dependencies()

    key = os.urandom(16)
    value = base64.b64encode(key).decode()
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
    key = os.urandom(16)
    value = base64.b64encode(key).decode()
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
