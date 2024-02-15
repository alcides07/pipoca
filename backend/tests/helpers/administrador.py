import base64
import os
from models.administrador import Administrador
from passlib.context import CryptContext
from main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

URL_AUTH = "/auth"


def create_administrador_helper(db: Session):
    key = os.urandom(16)
    value = base64.b64encode(key).decode()
    password = pwd_context.hash(value)

    admin = Administrador(
        username=value,
        email=f"{value}@email.com",
        password=password
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    token = login_administrador_helper(value, value)

    return token


def login_administrador_helper(username, password):
    token: str = client.post(
        URL_AUTH,
        data={
            "username": username,
            "password": password
        },
    ).json().get("access_token")

    return token
