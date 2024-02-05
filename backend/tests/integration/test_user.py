from tests.helpers.user import URL_USER, create_user_helper
from backend.main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies
from passlib.context import CryptContext

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_read_user_unit():
    remove_dependencies()

    user, token = create_user_helper()
    user = user.json().get("data")

    user_id = user.get("id")
    response = client.get(
        f"{URL_USER}/{user_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

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
    user, _ = create_user_helper()

    assert user.status_code == 201
