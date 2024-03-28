import os
import base64
from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.user import URL_USER, create_user_helper, login_user_helper
from main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies
from passlib.context import CryptContext

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_read_user_unit():
    remove_dependencies()

    response, token, _ = create_user_helper()
    user = response.json().get("data")

    user_id = user.get("id")
    response = client.get(
        f"{URL_USER}/{user_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_user_unit_admin():
    remove_dependencies()

    response_user, _, _ = create_user_helper()
    user_id = response_user.json().get("data").get("id")

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.get(
        f"{URL_USER}/{user_id}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_meus_dados_admin():
    remove_dependencies()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.get(
        f"{URL_USER}/eu/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response.status_code == 501

    resume_dependencies()


def test_read_meus_dados_user():
    remove_dependencies()

    _, token, _ = create_user_helper()

    response = client.get(
        f"{URL_USER}/eu/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_imagem_user():
    remove_dependencies()

    response_user, token, _ = create_user_helper()
    user_id = response_user.json().get("data").get("id")

    with open("./tests/integration/user.png", 'rb') as file:
        client.post(
            f"{URL_USER}/{user_id}/imagem/",
            files={"imagem": file},
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    response = client.get(
        f"{URL_USER}/{user_id}/imagem/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_imagem_inexistente_user():
    remove_dependencies()

    response_user, token, _ = create_user_helper()
    user_id = response_user.json().get("data").get("id")

    response = client.get(
        f"{URL_USER}/{user_id}/imagem/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

    resume_dependencies()


def test_delete_imagem_user():
    remove_dependencies()

    response_user, token, _ = create_user_helper()
    user_id = response_user.json().get("data").get("id")

    with open("./tests/integration/user.png", 'rb') as file:
        client.post(
            f"{URL_USER}/{user_id}/imagem/",
            files={"imagem": file},
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    response = client.delete(
        f"{URL_USER}/{user_id}/imagem/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204

    resume_dependencies()


def test_delete_imagem_inexistente_user():
    remove_dependencies()

    response_user, token, _ = create_user_helper()
    user_id = response_user.json().get("data").get("id")

    response = client.delete(
        f"{URL_USER}/{user_id}/imagem/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 404

    resume_dependencies()


def test_read_users_user():
    remove_dependencies()

    _, token_user, _ = create_user_helper()

    response_user = client.get(
        URL_USER,
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )
    assert response_user.status_code == 401

    resume_dependencies()


def test_read_users_admin():
    remove_dependencies()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response_admin = client.get(
        URL_USER,
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response_admin.status_code == 200

    resume_dependencies()


def test_create_user():
    remove_dependencies()

    response, _, _ = create_user_helper()

    assert response.status_code == 201

    resume_dependencies()


def test_create_user_email_exists():
    remove_dependencies()

    key = os.urandom(16)
    value = base64.b64encode(key).decode()
    password = pwd_context.hash(value)

    JSON_USER = {
        "username": value,
        "email": f"{value}@email.com",
        "password": password,
        "passwordConfirmation": password
    }

    user = client.post(
        URL_USER,
        json=JSON_USER
    )

    assert user.status_code == 201

    user_repeat = JSON_USER
    user_repeat["username"] = "unique_username"

    response = client.post(
        URL_USER,
        json=user_repeat
    )

    assert response.status_code == 400

    resume_dependencies()


def test_create_user_username_exists():
    remove_dependencies()

    key = os.urandom(16)
    value = base64.b64encode(key).decode()
    password = pwd_context.hash(value)

    JSON_USER = {
        "username": value,
        "email": f"{value}@email.com",
        "password": password,
        "passwordConfirmation": password
    }

    user = client.post(
        URL_USER,
        json=JSON_USER
    )
    assert user.status_code == 201

    user_repeat = JSON_USER
    user_repeat["email"] = "unique_email@email.com"

    response = client.post(
        URL_USER,
        json=user_repeat
    )

    assert response.status_code == 400

    resume_dependencies()


def test_create_imagem_user():
    remove_dependencies()

    response_user, token, _ = create_user_helper()
    user_id = response_user.json().get("data").get("id")

    with open("./tests/integration/user.png", 'rb') as file:
        response = client.post(
            f"{URL_USER}/{user_id}/imagem/",
            files={"imagem": file},
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert response.status_code == 200

    resume_dependencies()


def test_update_full_user_username_exists():
    remove_dependencies()

    response, _, JSON_USER = create_user_helper()
    key = os.urandom(16)
    value = base64.b64encode(key).decode()

    assert response.status_code == 201

    user_repeat = JSON_USER.copy()
    user_repeat["username"] = value
    user_repeat["email"] = f"{value}@email.com"

    user_repeat_response = client.post(
        URL_USER,
        json=user_repeat
    )

    assert user_repeat_response.status_code == 201

    token = login_user_helper(user_repeat["username"], user_repeat["password"])
    user_repeat["username"] = JSON_USER["username"]
    user_id = user_repeat_response.json().get("data").get("id")

    response = client.put(
        f"{URL_USER}/{user_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=user_repeat
    )

    assert response.status_code == 400

    resume_dependencies()


def test_update_full_user_email_exists():
    remove_dependencies()

    response, _, JSON_USER = create_user_helper()
    key = os.urandom(16)
    value = base64.b64encode(key).decode()

    assert response.status_code == 201

    user_repeat = JSON_USER.copy()
    user_repeat["username"] = value
    user_repeat["email"] = f"{value}@email.com"

    user_repeat_response = client.post(
        URL_USER,
        json=user_repeat
    )

    assert user_repeat_response.status_code == 201

    token = login_user_helper(user_repeat["username"], user_repeat["password"])
    user_repeat["email"] = JSON_USER["email"]
    user_id = user_repeat_response.json().get("data").get("id")

    response = client.put(
        f"{URL_USER}/{user_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=user_repeat
    )

    assert response.status_code == 400

    resume_dependencies()


def test_update_partial_user_by_user():
    remove_dependencies()

    key = os.urandom(16)
    value = base64.b64encode(key).decode()
    response_user, token, _ = create_user_helper()
    user_id = response_user.json().get("data").get("id")

    JSON_USER_PARCIAL = {
        "email": f"{value}@email.com"
    }

    response = client.patch(
        f"{URL_USER}/{user_id}/",
        json=JSON_USER_PARCIAL,
        headers={
            "Authorization": f"Bearer {token}",
        }
    )

    assert response.status_code == 200

    resume_dependencies()


def test_update_partial_user_by_admin():
    remove_dependencies()

    key = os.urandom(16)
    value = base64.b64encode(key).decode()
    response_user, _, _ = create_user_helper()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)
    user_id = response_user.json().get("data").get("id")

    JSON_USER_PARCIAL = {
        "email": f"{value}@email.com"
    }

    response = client.patch(
        f"{URL_USER}/{user_id}/",
        json=JSON_USER_PARCIAL,
        headers={
            "Authorization": f"Bearer {token_admin}",
        }
    )

    assert response.status_code == 200

    resume_dependencies()
