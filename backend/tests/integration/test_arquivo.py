from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.arquivo import URL_ARQUIVO, create_arquivo_admin_helper, create_arquivo_user_helper, update_full_arquivo_helper, update_partial_arquivo_helper
from tests.helpers.user import create_user_helper
from backend.main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)


def test_read_arquivo_unit_user():
    remove_dependencies()

    response_arquivo_user, token = create_arquivo_user_helper()
    arquivo_id = response_arquivo_user.json().get("data").get("id")

    response = client.get(
        f"{URL_ARQUIVO}/{arquivo_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_arquivo_unit_admin():
    remove_dependencies()

    response_arquivo_admin, token = create_arquivo_admin_helper()
    arquivo_id = response_arquivo_admin.json().get("data").get("id")

    response = client.get(
        f"{URL_ARQUIVO}/{arquivo_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_arquivos_user():
    remove_dependencies()

    _, token_user, _ = create_user_helper()

    response_user = client.get(
        "/arquivos",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )
    assert response_user.status_code == 401

    resume_dependencies()


def test_read_arquivos_admin():
    remove_dependencies()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response_admin = client.get(
        "/arquivos",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )
    assert response_admin.status_code == 200

    resume_dependencies()


def test_create_arquivo_user():
    remove_dependencies()

    response, _ = create_arquivo_user_helper()

    assert response.status_code == 201

    resume_dependencies()


def test_create_arquivo_admin():
    remove_dependencies()

    response, _ = create_arquivo_admin_helper()

    assert response.status_code == 201

    resume_dependencies()


def test_delete_arquivo_user():
    remove_dependencies()

    response_arquivo_user, token = create_arquivo_user_helper()
    arquivo_id = response_arquivo_user.json().get("data").get("id")

    response = client.delete(
        f"{URL_ARQUIVO}/{arquivo_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_delete_arquivo_admin():
    remove_dependencies()

    response_arquivo_admin, token = create_arquivo_admin_helper()
    arquivo_id = response_arquivo_admin.json().get("data").get("id")

    response = client.delete(
        f"{URL_ARQUIVO}/{arquivo_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_update_partial_arquivo_user():
    remove_dependencies()

    response_arquivo_user, arquivo_antigo = update_partial_arquivo_helper()

    assert response_arquivo_user.status_code == 200

    response_json = response_arquivo_user.json().get("data")

    assert response_json.get("corpo") != arquivo_antigo.get("corpo")

    resume_dependencies()


def test_update_partial_arquivo_admin():
    remove_dependencies()

    response_arquivo_user, arquivo_antigo = update_partial_arquivo_helper(
        "admin")

    assert response_arquivo_user.status_code == 200

    response_json = response_arquivo_user.json().get("data")

    assert response_json.get("corpo") != arquivo_antigo.get("corpo")

    resume_dependencies()


def test_update_full_arquivo_user():
    remove_dependencies()

    response_arquivo_user, arquivo_antigo = update_full_arquivo_helper()

    assert response_arquivo_user.status_code == 200

    response_json = response_arquivo_user.json().get("data")

    assert response_json.get("nome") != arquivo_antigo.get("nome")
    assert response_json.get("secao") != arquivo_antigo.get("secao")
    assert response_json.get("status") != arquivo_antigo.get("status")
    assert response_json.get("corpo") != arquivo_antigo.get("corpo")

    resume_dependencies()


def test_update_full_arquivo_admin():
    remove_dependencies()

    response_arquivo_user, arquivo_antigo = update_full_arquivo_helper(
        "admin")

    assert response_arquivo_user.status_code == 200

    response_json = response_arquivo_user.json().get("data")

    assert response_json.get("nome") != arquivo_antigo.get("nome")
    assert response_json.get("secao") != arquivo_antigo.get("secao")
    assert response_json.get("status") != arquivo_antigo.get("status")
    assert response_json.get("corpo") != arquivo_antigo.get("corpo")

    resume_dependencies()
