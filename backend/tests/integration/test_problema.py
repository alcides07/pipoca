from passlib.context import CryptContext
from tests.helpers.problema import URL_PROBLEMA, create_problema_helper
from tests.helpers.user import create_user_helper
from backend.main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_read_problema_unit():
    remove_dependencies()

    problema, token = create_problema_helper()

    problema_id = problema.json().get("data").get("id")
    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas():
    remove_dependencies()

    response = client.get(
        URL_PROBLEMA,
    )

    assert response.status_code == 200

    resume_dependencies()


def test_create_problema():
    remove_dependencies()

    problema, _ = create_problema_helper()

    assert problema.status_code == 201

    resume_dependencies()


def test_update_partial_problema():
    remove_dependencies()

    problema, token = create_problema_helper()
    problema = problema.json().get("data")
    problema_id = problema.get("id")

    json_partial = {
        "nome": "NovoNome",
        "tags": ["Tag1, Tag2"]
    }

    response = client.patch(
        f"{URL_PROBLEMA}/{problema_id}/",
        json=json_partial,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    response_json = response.json().get("data")

    assert response_json.get(
        "nome") != problema.get("nome")

    assert response_json.get(
        "tags") != problema.get("tags")

    assert response_json.get(
        "tempo_limite") == problema.get("tempo_limite")

    resume_dependencies()


def test_update_full_problema_success():
    remove_dependencies()

    problema, token = create_problema_helper()
    problema = problema.json().get("data")
    problema_id = problema.get("id")

    problema_copy = problema.copy()

    problema["nome"] = "PUT"
    problema["nome_arquivo_entrada"] = "PUT"
    problema["nome_arquivo_saida"] = "PUT"
    problema.pop("tags")

    response = client.put(
        f"{URL_PROBLEMA}/{problema_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=problema
    )

    assert response.status_code == 200

    response_json = response.json().get("data")

    assert response_json.get("nome") != problema_copy.get("nome")

    assert response_json.get(
        "nome_arquivo_entrada") != problema_copy.get("nome_arquivo_entrada")

    assert response_json.get(
        "nome_arquivo_saida") != problema_copy.get("nome_arquivo_saida")

    assert response_json.get(
        "tempo_limite") == problema_copy.get("tempo_limite")

    assert response_json.get(
        "memoria_limite") == problema_copy.get("memoria_limite")

    resume_dependencies()


def test_update_full_problema_fail():
    remove_dependencies()

    problema, token = create_problema_helper()

    problema_id = problema.json().get("data").get("id")

    json_full_fake = {
        "nome": "nome",
    }

    response_put = client.put(
        f"{URL_PROBLEMA}/{problema_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_full_fake
    )

    assert response_put.status_code == 422

    resume_dependencies()


def test_upload_problema():
    remove_dependencies()

    _, token = create_user_helper()

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
