from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.user import create_user_helper
from tests.helpers.verificador import create_verificador_admin_helper, create_verificador_user_helper
from backend.main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)
URL_VERIFICADOR = "/verificadores"


def test_read_verificadores_user():
    remove_dependencies()

    _, token_user, _ = create_user_helper()

    response_user = client.get(
        URL_VERIFICADOR,
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )
    assert response_user.status_code == 401

    resume_dependencies()


def test_read_verificadores_admin():
    remove_dependencies()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response_admin = client.get(
        URL_VERIFICADOR,
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response_admin.status_code == 200

    resume_dependencies()


def test_read_verificador_unit_user():
    remove_dependencies()

    response_verificador, token = create_verificador_user_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    response = client.get(
        f"{URL_VERIFICADOR}/{verificador_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_verificador_unit_admin():
    remove_dependencies()

    response_verificador, token = create_verificador_admin_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    response = client.get(
        f"{URL_VERIFICADOR}/{verificador_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_create_verificador_user():
    remove_dependencies()

    response, _ = create_verificador_user_helper()

    assert response.status_code == 201

    resume_dependencies()


def test_create_verificador_admin():
    remove_dependencies()

    response, _ = create_verificador_admin_helper()

    assert response.status_code == 201

    resume_dependencies()


def test_delete_verificador_user():
    remove_dependencies()

    response_verificador, token = create_verificador_user_helper()

    verificador_id = response_verificador.json().get("data").get("id")

    response = client.delete(
        f"{URL_VERIFICADOR}/{verificador_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        }
    )

    assert response.status_code == 200

    resume_dependencies()


def test_delete_verificador_admin():
    remove_dependencies()

    response_verificador, token = create_verificador_admin_helper()

    verificador_id = response_verificador.json().get("data").get("id")

    response = client.delete(
        f"{URL_VERIFICADOR}/{verificador_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        }
    )

    assert response.status_code == 200

    resume_dependencies()
