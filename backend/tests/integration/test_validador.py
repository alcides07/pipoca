from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.user import create_user_helper
from tests.helpers.validador import create_validador_helper, update_full_validador_helper, update_partial_validador_helper
from main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)
URL_VALIDADOR = "/validadores"


def test_read_validadores_user():
    remove_dependencies()

    _, token_user, _ = create_user_helper()

    response_user = client.get(
        URL_VALIDADOR,
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )
    assert response_user.status_code == 401

    resume_dependencies()


def test_read_validadores_admin():
    remove_dependencies()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response_admin = client.get(
        URL_VALIDADOR,
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response_admin.status_code == 200

    resume_dependencies()


def test_read_validador_unit_user():
    remove_dependencies()

    response_validador, token = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    response = client.get(
        f"{URL_VALIDADOR}/{validador_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_validador_unit_admin():
    remove_dependencies()

    response_validador, token = create_validador_helper("admin")
    validador_id = response_validador.json().get("data").get("id")

    response = client.get(
        f"{URL_VALIDADOR}/{validador_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_create_validador_user():
    remove_dependencies()

    response, _ = create_validador_helper()

    assert response.status_code == 201

    resume_dependencies()


def test_create_validador_admin():
    remove_dependencies()

    response, _ = create_validador_helper("admin")

    assert response.status_code == 201

    resume_dependencies()


def test_update_partial_validador_user():
    remove_dependencies()

    response_validador_user, validador_antigo = update_partial_validador_helper()

    assert response_validador_user.status_code == 200

    response_json = response_validador_user.json().get("data")

    assert response_json.get("corpo") != validador_antigo.get("corpo")

    resume_dependencies()


def test_update_partial_validador_admin():
    remove_dependencies()

    response_validador_user, validador_antigo = update_partial_validador_helper(
        "admin")

    assert response_validador_user.status_code == 200

    response_json = response_validador_user.json().get("data")

    assert response_json.get("corpo") != validador_antigo.get("corpo")

    resume_dependencies()


def test_update_full_validador_user():
    remove_dependencies()

    response_validador_user, validador_antigo = update_full_validador_helper()

    assert response_validador_user.status_code == 200

    response_json = response_validador_user.json().get("data")

    assert response_json.get("nome") != validador_antigo.get("nome")
    assert response_json.get(
        "linguagem") != validador_antigo.get("linguagem")
    assert response_json.get("corpo") != validador_antigo.get("corpo")

    resume_dependencies()


def test_update_full_validador_admin():
    remove_dependencies()

    response_validador_user, validador_antigo = update_full_validador_helper(
        "admin")

    assert response_validador_user.status_code == 200

    response_json = response_validador_user.json().get("data")

    assert response_json.get("nome") != validador_antigo.get("nome")
    assert response_json.get(
        "linguagem") != validador_antigo.get("linguagem")
    assert response_json.get("corpo") != validador_antigo.get("corpo")

    resume_dependencies()


def test_delete_validador_user():
    remove_dependencies()

    response_validador, token = create_validador_helper()

    validador_id = response_validador.json().get("data").get("id")

    response = client.delete(
        f"{URL_VALIDADOR}/{validador_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        }
    )

    assert response.status_code == 204

    resume_dependencies()


def test_delete_validador_admin():
    remove_dependencies()

    response_validador, token = create_validador_helper("admin")

    validador_id = response_validador.json().get("data").get("id")

    response = client.delete(
        f"{URL_VALIDADOR}/{validador_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        }
    )

    assert response.status_code == 204

    resume_dependencies()
