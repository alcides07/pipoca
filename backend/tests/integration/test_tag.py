from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.problema import create_problema_user_helper
from tests.helpers.tag import JSON_TAG, URL_TAG, create_only_tag_helper, create_tag_in_problema_helper
from tests.helpers.user import create_user_helper
from main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)


# -------------------------------
# Testes de leitura (GET)
# -------------------------------
def test_read_tag_all():
    remove_dependencies()

    _, token, _ = create_user_helper()

    response = client.get(
        URL_TAG,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_tag_by_id():
    remove_dependencies()

    response_tag, token = create_only_tag_helper()
    tag_id = response_tag.json().get("data").get("id")

    response = client.get(
        f"{URL_TAG}/{tag_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


# -------------------------------
# Testes de escrita (POST)
# -------------------------------
def test_create_only_tag_com_user():
    remove_dependencies()

    response_tag, _ = create_only_tag_helper()

    assert response_tag.status_code == 201

    resume_dependencies()


def test_create_tag_in_problema_com_user_criador_do_problema():
    remove_dependencies()

    response_problema, token = create_problema_user_helper()
    problema_id = response_problema.json().get("data").get("id")

    response_tag = create_tag_in_problema_helper(
        token, problema_id)

    assert response_tag.status_code == 201

    resume_dependencies()


def test_create_tag_in_problema_com_user_nao_criador_do_problema():
    remove_dependencies()

    response_problema, _ = create_problema_user_helper()
    problema_id = response_problema.json().get("data").get("id")

    _, token, _ = create_user_helper()

    response_tag = create_tag_in_problema_helper(
        token, problema_id)

    assert response_tag.status_code == 401

    resume_dependencies()


# -------------------------------
# Testes de atualização parcial (PATCH)
# -------------------------------
def test_update_partial_tag_com_user_negado():
    remove_dependencies()

    response_tag, token = create_only_tag_helper()
    tag_id = response_tag.json().get("data").get("id")

    json = JSON_TAG.copy()
    json["nome"] = "newTag"

    response = client.patch(
        f"{URL_TAG}/{tag_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json
    )

    assert response.status_code == 401

    resume_dependencies()


def test_update_partial_tag_com_admin():
    remove_dependencies()

    response_tag, _ = create_only_tag_helper()
    tag_id = response_tag.json().get("data").get("id")

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    json = JSON_TAG.copy()
    json["nome"] = "newTag"

    response = client.patch(
        f"{URL_TAG}/{tag_id}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
        json=json
    )

    assert response.status_code == 200

    resume_dependencies()


# -------------------------------
# Testes de atualização total (PUT)
# -------------------------------
def test_update_full_tag_com_user_negado():
    remove_dependencies()

    response_tag, token = create_only_tag_helper()
    tag_id = response_tag.json().get("data").get("id")

    json = JSON_TAG.copy()
    json["nome"] = "newTag"

    response = client.put(
        f"{URL_TAG}/{tag_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json
    )

    assert response.status_code == 401

    resume_dependencies()


def test_update_full_tag_com_admin():
    remove_dependencies()

    response_tag, _ = create_only_tag_helper()
    tag_id = response_tag.json().get("data").get("id")

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    json = JSON_TAG.copy()
    json["nome"] = "newTag"

    response = client.put(
        f"{URL_TAG}/{tag_id}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
        json=json
    )

    assert response.status_code == 200

    resume_dependencies()


# -------------------------------
# Testes de exclusão (DELETE)
# -------------------------------
def test_delete_tag_com_user_negado():
    remove_dependencies()

    response_tag, token = create_only_tag_helper()
    tag_id = response_tag.json().get("data").get("id")

    response = client.delete(
        f"{URL_TAG}/{tag_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        }
    )

    assert response.status_code == 401

    resume_dependencies()


def test_delete_tag_com_admin():
    remove_dependencies()

    response_tag, _ = create_only_tag_helper()
    tag_id = response_tag.json().get("data").get("id")

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.delete(
        f"{URL_TAG}/{tag_id}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        }
    )

    assert response.status_code == 204

    resume_dependencies()
