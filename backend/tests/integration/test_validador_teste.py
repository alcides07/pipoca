from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.user import create_user_helper
from main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies
from tests.helpers.validador import create_validador_helper


client = TestClient(app)
URL_VALIDADOR_TESTES = "/validadoresTestes"


def test_read_validador_testes_user():
    remove_dependencies()

    _, token_user, _ = create_user_helper()

    response_user = client.get(
        URL_VALIDADOR_TESTES,
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )
    assert response_user.status_code == 401

    resume_dependencies()


def test_read_validador_testes_admin():
    remove_dependencies()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response_admin = client.get(
        URL_VALIDADOR_TESTES,
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response_admin.status_code == 200

    resume_dependencies()


def test_read_validador_teste_unit_dono_user():
    remove_dependencies()

    response_validador, token = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    response_validador_teste = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_validador_teste
    )
    validador_teste_id = response_validador_teste.json().get("data").get("id")

    response = client.get(
        f"{URL_VALIDADOR_TESTES}/{validador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_validador_teste_unit_nao_dono_user():
    remove_dependencies()

    response_validador, token = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    response_validador_teste = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_validador_teste
    )
    validador_teste_id = response_validador_teste.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_VALIDADOR_TESTES}/{validador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_validador_teste_unit_admin_user():
    remove_dependencies()

    response_validador, token = create_validador_helper("admin")
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    response_validador_teste = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_validador_teste
    )
    validador_teste_id = response_validador_teste.json().get("data").get("id")

    response = client.get(
        f"{URL_VALIDADOR_TESTES}/{validador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_create_validador_teste_user():
    remove_dependencies()

    response_validador, token = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    response = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_validador_teste
    )
    assert response.status_code == 201

    resume_dependencies()


def test_create_validador_teste_admin():
    remove_dependencies()

    response_validador, _ = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
        json=json_validador_teste
    )
    assert response.status_code == 201

    resume_dependencies()


def test_update_partial_validador_teste_dono():
    remove_dependencies()

    response_validador, token = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    response_validador_teste = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_validador_teste
    )
    validador_teste_id = response_validador_teste.json().get("data").get("id")

    json_partial = {
        "entrada": "newEntrada"
    }

    response = client.patch(
        f"{URL_VALIDADOR_TESTES}/{validador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_partial
    )

    assert response.status_code == 200

    resume_dependencies()


def test_update_partial_validador_teste_nao_dono():
    remove_dependencies()

    response_validador, token = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    response_validador_teste = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_validador_teste
    )
    validador_teste_id = response_validador_teste.json().get("data").get("id")

    json_partial = {
        "entrada": "newEntrada"
    }

    _, token_user, _ = create_user_helper()

    response = client.patch(
        f"{URL_VALIDADOR_TESTES}/{validador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
        json=json_partial
    )

    assert response.status_code == 401

    resume_dependencies()


def test_update_partial_validador_teste_admin():
    remove_dependencies()

    response_validador, token = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    response_validador_teste = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_validador_teste
    )
    validador_teste_id = response_validador_teste.json().get("data").get("id")

    json_partial = {
        "entrada": "newEntrada"
    }

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.patch(
        f"{URL_VALIDADOR_TESTES}/{validador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
        json=json_partial
    )

    assert response.status_code == 200

    resume_dependencies()


def test_update_total_validador_teste_dono():
    remove_dependencies()

    response_validador, token = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    response_validador_teste = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_validador_teste
    )
    validador_teste_id = response_validador_teste.json().get("data").get("id")

    json_total = {
        "numero": 99,
        "veredito": "valid",
        "entrada": "new"
    }

    response = client.put(
        f"{URL_VALIDADOR_TESTES}/{validador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_total
    )

    assert response.status_code == 200

    resume_dependencies()


def test_update_total_validador_teste_nao_dono():
    remove_dependencies()

    response_validador, token = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    response_validador_teste = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_validador_teste
    )
    validador_teste_id = response_validador_teste.json().get("data").get("id")

    json_total = {
        "numero": 99,
        "veredito": "invalid",
        "entrada": "new"
    }

    _, token_user, _ = create_user_helper()

    response = client.put(
        f"{URL_VALIDADOR_TESTES}/{validador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
        json=json_total
    )

    assert response.status_code == 401

    resume_dependencies()


def test_update_total_validador_teste_admin():
    remove_dependencies()

    response_validador, token = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    response_validador_teste = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_validador_teste
    )
    validador_teste_id = response_validador_teste.json().get("data").get("id")

    json_total = {
        "numero": 99,
        "veredito": "valid",
        "entrada": "new"
    }

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.put(
        f"{URL_VALIDADOR_TESTES}/{validador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
        json=json_total
    )

    assert response.status_code == 200

    resume_dependencies()


def test_delete_validador_teste_dono():
    remove_dependencies()

    response_validador, token = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    response_validador_teste = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_validador_teste
    )
    validador_teste_id = response_validador_teste.json().get("data").get("id")

    response = client.delete(
        f"{URL_VALIDADOR_TESTES}/{validador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204

    resume_dependencies()


def test_delete_validador_teste_nao_dono():
    remove_dependencies()

    response_validador, token = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    response_validador_teste = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_validador_teste
    )
    validador_teste_id = response_validador_teste.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.delete(
        f"{URL_VALIDADOR_TESTES}/{validador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_delete_validador_teste_admin():
    remove_dependencies()

    response_validador, token = create_validador_helper()
    validador_id = response_validador.json().get("data").get("id")

    json_validador_teste = JSON_VALIDADOR_TESTE.copy()
    json_validador_teste["validador_id"] = validador_id

    response_validador_teste = client.post(
        f"{URL_VALIDADOR_TESTES}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_validador_teste
    )
    validador_teste_id = response_validador_teste.json().get("data").get("id")

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.delete(
        f"{URL_VALIDADOR_TESTES}/{validador_teste_id}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response.status_code == 204

    resume_dependencies()


JSON_VALIDADOR_TESTE = {
    "numero": 1,
    "veredito": "valid",
    "entrada": "string",
    "validador_id": 0
}
