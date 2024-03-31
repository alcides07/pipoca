import base64
import os
from passlib.context import CryptContext
from main import app
from fastapi.testclient import TestClient
from datetime import timedelta
from utils.create_token import create_token

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

URL_USER = "/usuarios"
URL_AUTH = "/auth"


def create_user_helper():
    key = os.urandom(16)
    value = base64.b64encode(key).decode()
    password = pwd_context.hash(value)
    JSON_USER = {
        "username": value,
        "email": f"{value}@email.com",
        "password": password,
        "passwordConfirmation": password
    }

    response = client.post(
        URL_USER,
        json=JSON_USER
    )

    activate_account_user_helper(JSON_USER["username"])

    token_login = login_user_helper(value, password)
    return response, token_login, JSON_USER


def activate_account_user_helper(username: str):
    access_token_expires = timedelta(minutes=5)
    token_ativacao = create_token(
        data={
            "sub": username
        },
        expires_delta=access_token_expires
    )

    client.get(
        f"{URL_AUTH}/ativacao/?codigo={token_ativacao}",
    )


def login_user_helper(username, password):
    token: str = client.post(
        URL_AUTH,
        data={
            "username": username,
            "password": password
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    ).json().get("access_token")

    return token
