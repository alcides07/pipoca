import base64
import os
from passlib.context import CryptContext
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

URL_USER = "/users"
URL_AUTH = "/auth"


def create_user_helper():
    key = os.urandom(16)
    value = base64.b64encode(key).decode()
    password = pwd_context.hash(value)

    user = client.post(
        URL_USER,
        json={
            "username": value,
            "email": f"{value}@email.com",
            "password": password,
            "passwordConfirmation": password
        }
    )

    token = client.post(
        URL_AUTH,
        data={
            "username": value,
            "password": password
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    ).json().get("access_token")

    return user, token
