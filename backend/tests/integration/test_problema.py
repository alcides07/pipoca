from passlib.context import CryptContext
from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.problema import URL_PROBLEMA, create_problema_admin_helper, create_problema_user_helper, update_full_problema_fail_incomplete, update_full_problema_success_helper, update_partial_problema_helper
from tests.helpers.user import create_user_helper
from backend.main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_read_problema_unit_user():
    remove_dependencies()

    response_problema_user, token = create_problema_user_helper()

    problema_id = response_problema_user.json().get("data").get("id")
    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problema_unit_admin():
    remove_dependencies()

    response_problema_admin, token = create_problema_admin_helper()

    problema_id = response_problema_admin.json().get("data").get("id")
    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas_user():
    remove_dependencies()

    _, token_user, _ = create_user_helper()

    response_problema_user = client.get(
        URL_PROBLEMA,
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )
    assert response_problema_user.status_code == 401

    resume_dependencies()


def test_read_problemas_admin():
    remove_dependencies()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response_problema_admin = client.get(
        URL_PROBLEMA,
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response_problema_admin.status_code == 200

    resume_dependencies()


def test_create_problema_user():
    remove_dependencies()

    response_problema_user, _ = create_problema_user_helper()

    assert response_problema_user.status_code == 201

    resume_dependencies()


def test_create_problema_admin():
    remove_dependencies()

    response_problema_admin, _ = create_problema_admin_helper()

    assert response_problema_admin.status_code == 201

    resume_dependencies()


def test_update_partial_problema_user():
    remove_dependencies()

    response_problema_user, problema = update_partial_problema_helper()

    assert response_problema_user.status_code == 200

    response_json = response_problema_user.json().get("data")

    assert response_json.get(
        "nome") != problema.get("nome")

    assert response_json.get(
        "tags") != problema.get("tags")

    assert response_json.get(
        "tempo_limite") == problema.get("tempo_limite")

    resume_dependencies()


def test_update_partial_problema_admin():
    remove_dependencies()

    response_problema_admin, problema = update_partial_problema_helper("admin")

    assert response_problema_admin.status_code == 200

    response_json = response_problema_admin.json().get("data")

    assert response_json.get(
        "nome") != problema.get("nome")

    assert response_json.get(
        "tags") != problema.get("tags")

    assert response_json.get(
        "tempo_limite") == problema.get("tempo_limite")

    resume_dependencies()


def test_update_full_problema_success_user():
    remove_dependencies()

    response_problema_user, problema = update_full_problema_success_helper()
    assert response_problema_user.status_code == 200

    response_json = response_problema_user.json().get("data")

    assert response_json.get("nome") != problema.get("nome")

    assert response_json.get(
        "nome_arquivo_entrada") != problema.get("nome_arquivo_entrada")

    assert response_json.get(
        "nome_arquivo_saida") != problema.get("nome_arquivo_saida")

    assert response_json.get(
        "tempo_limite") == problema.get("tempo_limite")

    assert response_json.get(
        "memoria_limite") == problema.get("memoria_limite")

    resume_dependencies()


def test_update_full_problema_success_admin():
    remove_dependencies()

    response_problema_user, problema = update_full_problema_success_helper(
        "admin")
    assert response_problema_user.status_code == 200

    response_json = response_problema_user.json().get("data")

    assert response_json.get("nome") != problema.get("nome")

    assert response_json.get(
        "nome_arquivo_entrada") != problema.get("nome_arquivo_entrada")

    assert response_json.get(
        "nome_arquivo_saida") != problema.get("nome_arquivo_saida")

    assert response_json.get(
        "tempo_limite") == problema.get("tempo_limite")

    assert response_json.get(
        "memoria_limite") == problema.get("memoria_limite")

    resume_dependencies()


def test_update_full_problema_fail_user():
    remove_dependencies()

    response = update_full_problema_fail_incomplete()

    assert response.status_code == 422

    resume_dependencies()


def test_update_full_problema_fail_admin():
    remove_dependencies()

    response = update_full_problema_fail_incomplete("admin")

    assert response.status_code == 422

    resume_dependencies()


def test_upload_problema_user():
    remove_dependencies()

    _, token, _ = create_user_helper()

    with open("./tests/integration/upload_problem.zip", 'rb') as file:
        response = client.post(
            f"{URL_PROBLEMA}/upload/",
            files={"pacote": file},
            data={"privado": "true"},
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert response.status_code == 201

    resume_dependencies()


def test_upload_problema_admin():
    remove_dependencies()

    database = next(get_db_test())
    token = create_administrador_helper(database)

    with open("./tests/integration/upload_problem.zip", 'rb') as file:
        response = client.post(
            f"{URL_PROBLEMA}/upload/",
            files={"pacote": file},
            data={"privado": "true"},
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert response.status_code == 201

    resume_dependencies()
