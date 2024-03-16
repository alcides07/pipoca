from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.user import create_user_helper
from main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies
from tests.helpers.verificador import create_verificador_helper

client = TestClient(app)
URL_VERIFICADOR_TESTES = "/verificadorTestes"


def test_read_verificador_testes_user():
    remove_dependencies()

    _, token_user, _ = create_user_helper()

    response_user = client.get(
        URL_VERIFICADOR_TESTES,
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )
    assert response_user.status_code == 401

    resume_dependencies()


def test_read_verificador_testes_admin():
    remove_dependencies()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response_admin = client.get(
        URL_VERIFICADOR_TESTES,
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response_admin.status_code == 200

    resume_dependencies()


def test_read_verificador_teste_unit_dono_user():
    remove_dependencies()

    response_verificador, token = create_verificador_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    response_verificador_teste = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_verificador_teste
    )
    verificador_teste_id = response_verificador_teste.json().get("data").get("id")

    response = client.get(
        f"{URL_VERIFICADOR_TESTES}/{verificador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_verificador_teste_unit_nao_dono_user():
    remove_dependencies()

    response_verificador, token = create_verificador_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    response_verificador_teste = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_verificador_teste
    )
    verificador_teste_id = response_verificador_teste.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_VERIFICADOR_TESTES}/{verificador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_verificador_teste_unit_admin_user():
    remove_dependencies()

    response_verificador, token = create_verificador_helper("admin")
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    response_verificador_teste = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_verificador_teste
    )
    verificador_teste_id = response_verificador_teste.json().get("data").get("id")

    response = client.get(
        f"{URL_VERIFICADOR_TESTES}/{verificador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_create_verificador_teste_user():
    remove_dependencies()

    response_verificador, token = create_verificador_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    response = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_verificador_teste
    )
    assert response.status_code == 201

    resume_dependencies()


def test_create_verificador_teste_admin():
    remove_dependencies()

    response_verificador, _ = create_verificador_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
        json=json_verificador_teste
    )
    assert response.status_code == 201

    resume_dependencies()


def test_update_partial_verificador_teste_dono():
    remove_dependencies()

    response_verificador, token = create_verificador_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    response_verificador_teste = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_verificador_teste
    )
    verificador_teste_id = response_verificador_teste.json().get("data").get("id")

    json_partial = {
        "entrada": "newEntrada"
    }

    response = client.patch(
        f"{URL_VERIFICADOR_TESTES}/{verificador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_partial
    )

    assert response.status_code == 200

    resume_dependencies()


def test_update_partial_verificador_teste_nao_dono():
    remove_dependencies()

    response_verificador, token = create_verificador_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    response_verificador_teste = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_verificador_teste
    )
    verificador_teste_id = response_verificador_teste.json().get("data").get("id")

    json_partial = {
        "entrada": "newEntrada"
    }

    _, token_user, _ = create_user_helper()

    response = client.patch(
        f"{URL_VERIFICADOR_TESTES}/{verificador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
        json=json_partial
    )

    assert response.status_code == 401

    resume_dependencies()


def test_update_partial_verificador_teste_admin():
    remove_dependencies()

    response_verificador, token = create_verificador_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    response_verificador_teste = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_verificador_teste
    )
    verificador_teste_id = response_verificador_teste.json().get("data").get("id")

    json_partial = {
        "entrada": "newEntrada"
    }

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.patch(
        f"{URL_VERIFICADOR_TESTES}/{verificador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
        json=json_partial
    )

    assert response.status_code == 200

    resume_dependencies()


def test_update_total_verificador_teste_dono():
    remove_dependencies()

    response_verificador, token = create_verificador_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    response_verificador_teste = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_verificador_teste
    )
    verificador_teste_id = response_verificador_teste.json().get("data").get("id")

    json_total = {
        "numero": 99,
        "veredito": "ok",
        "entrada": "new"
    }

    response = client.put(
        f"{URL_VERIFICADOR_TESTES}/{verificador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_total
    )

    assert response.status_code == 200

    resume_dependencies()


def test_update_total_verificador_teste_nao_dono():
    remove_dependencies()

    response_verificador, token = create_verificador_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    response_verificador_teste = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_verificador_teste
    )
    verificador_teste_id = response_verificador_teste.json().get("data").get("id")

    json_total = {
        "numero": 99,
        "veredito": "ok",
        "entrada": "new"
    }

    _, token_user, _ = create_user_helper()

    response = client.put(
        f"{URL_VERIFICADOR_TESTES}/{verificador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
        json=json_total
    )

    assert response.status_code == 401

    resume_dependencies()


def test_update_total_verificador_teste_admin():
    remove_dependencies()

    response_verificador, token = create_verificador_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    response_verificador_teste = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_verificador_teste
    )
    verificador_teste_id = response_verificador_teste.json().get("data").get("id")

    json_total = {
        "numero": 99,
        "veredito": "ok",
        "entrada": "new"
    }

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.put(
        f"{URL_VERIFICADOR_TESTES}/{verificador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
        json=json_total
    )

    assert response.status_code == 200

    resume_dependencies()


def test_delete_verificador_teste_dono():
    remove_dependencies()

    response_verificador, token = create_verificador_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    response_verificador_teste = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_verificador_teste
    )
    verificador_teste_id = response_verificador_teste.json().get("data").get("id")

    response = client.delete(
        f"{URL_VERIFICADOR_TESTES}/{verificador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204

    resume_dependencies()


def test_delete_verificador_teste_nao_dono():
    remove_dependencies()

    response_verificador, token = create_verificador_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    response_verificador_teste = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_verificador_teste
    )
    verificador_teste_id = response_verificador_teste.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.delete(
        f"{URL_VERIFICADOR_TESTES}/{verificador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_delete_verificador_teste_admin():
    remove_dependencies()

    response_verificador, token = create_verificador_helper()
    verificador_id = response_verificador.json().get("data").get("id")

    json_verificador_teste = JSON_VERIFICADOR_TESTE.copy()
    json_verificador_teste["verificador_id"] = verificador_id

    response_verificador_teste = client.post(
        f"{URL_VERIFICADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_verificador_teste
    )
    verificador_teste_id = response_verificador_teste.json().get("data").get("id")

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.delete(
        f"{URL_VERIFICADOR_TESTES}/{verificador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response.status_code == 204

    resume_dependencies()


JSON_VERIFICADOR_TESTE = {
    "numero": 1,
    "veredito": "ok",
    "entrada": "string",
    "verificador_id": 0
}
