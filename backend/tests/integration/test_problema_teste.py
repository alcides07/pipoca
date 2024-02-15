from tests.helpers.problema import create_problema_user_helper
from tests.helpers.problema import JSON_PROBLEMA
from tests.helpers.user import create_user_helper
from backend.main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)
URL_PROBLEMA_TESTE = "/problemaTestes"


def test_read_problema_teste_unit_sou_criador_do_problema():
    remove_dependencies()

    response_problema, token_autor_problema = create_problema_user_helper()
    problema_id = response_problema.json().get("data").get("id")

    problema_teste = JSON_PROBLEMA_TESTE.copy()
    problema_teste["problema_id"] = problema_id

    response_problema_teste = client.post(
        URL_PROBLEMA_TESTE,
        json=problema_teste,
        headers={
            "Authorization": f"Bearer {token_autor_problema}",
        },
    )

    id_problema_teste = response_problema_teste.json().get("data").get("id")

    response = client.get(
        f"{URL_PROBLEMA_TESTE}/{id_problema_teste}/",
        headers={
            "Authorization": f"Bearer {token_autor_problema}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problema_teste_unit_nao_sou_criador_do_problema_publico_e_o_teste_nao_eh_de_exemplo():
    remove_dependencies()

    json_problema = JSON_PROBLEMA.copy()
    json_problema["privado"] = False

    response_problema, token_autor_problema = create_problema_user_helper()
    problema_id = response_problema.json().get("data").get("id")

    problema_teste = JSON_PROBLEMA_TESTE.copy()
    problema_teste["problema_id"] = problema_id
    problema_teste["exemplo"] = False

    response_problema_teste = client.post(
        URL_PROBLEMA_TESTE,
        json=problema_teste,
        headers={
            "Authorization": f"Bearer {token_autor_problema}",
        },
    )

    id_problema_teste = response_problema_teste.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_PROBLEMA_TESTE}/{id_problema_teste}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_problema_teste_unit_nao_sou_criador_do_problema_privado_e_o_teste_eh_de_exemplo():
    remove_dependencies()

    json_problema = JSON_PROBLEMA.copy()
    json_problema["privado"] = True

    response_problema, token_autor_problema = create_problema_user_helper()
    problema_id = response_problema.json().get("data").get("id")

    problema_teste = JSON_PROBLEMA_TESTE.copy()
    problema_teste["problema_id"] = problema_id
    problema_teste["exemplo"] = True

    response_problema_teste = client.post(
        URL_PROBLEMA_TESTE,
        json=problema_teste,
        headers={
            "Authorization": f"Bearer {token_autor_problema}",
        },
    )

    id_problema_teste = response_problema_teste.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_PROBLEMA_TESTE}/{id_problema_teste}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_create_problema_teste():
    remove_dependencies()

    response_problema_criado, token_autor_problema = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    problema_teste = JSON_PROBLEMA_TESTE.copy()
    problema_teste["problema_id"] = problema_id

    response = client.post(
        URL_PROBLEMA_TESTE,
        json=problema_teste,
        headers={
            "Authorization": f"Bearer {token_autor_problema}",
        },
    )

    assert response.status_code == 201

    resume_dependencies()


def test_create_problema_teste_unit_nao_sou_criador_do_problema():
    remove_dependencies()

    response_problema_criado, _ = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    problema_teste = JSON_PROBLEMA_TESTE.copy()
    problema_teste["problema_id"] = problema_id

    _, token_user, _ = create_user_helper()

    response = client.post(
        URL_PROBLEMA_TESTE,
        json=problema_teste,
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_create_problema_test_unit_com_teste_com_numero_repetido():
    remove_dependencies()

    json_problema = JSON_PROBLEMA.copy()
    json_problema["testes"][0]["numero"] = 99

    response_problema_criado, token_criador = create_problema_user_helper(
        json_problema)
    problema_id = response_problema_criado.json().get("data").get("id")

    problema_teste = JSON_PROBLEMA_TESTE.copy()
    problema_teste["problema_id"] = problema_id
    problema_teste["numero"] = 99

    response = client.post(
        URL_PROBLEMA_TESTE,
        json=problema_teste,
        headers={
            "Authorization": f"Bearer {token_criador}",
        },
    )

    assert response.status_code == 400

    resume_dependencies()


def test_update_problema_teste_nao_sou_dono():
    remove_dependencies()

    response_problema, token_autor_problema = create_problema_user_helper()
    problema_id = response_problema.json().get("data").get("id")

    problema_teste = JSON_PROBLEMA_TESTE.copy()
    problema_teste["problema_id"] = problema_id

    response_problema_teste = client.post(
        URL_PROBLEMA_TESTE,
        json=problema_teste,
        headers={
            "Authorization": f"Bearer {token_autor_problema}",
        },
    )

    id_problema_teste = response_problema_teste.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.patch(
        f"{URL_PROBLEMA_TESTE}/{id_problema_teste}/",
        json={
            "descricao": "novaDescricao"
        },
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_update_partial_problema_teste_com_numeros_repetidos():
    remove_dependencies()

    json_problema = JSON_PROBLEMA.copy()
    json_problema["testes"][0]["numero"] = 97
    json_problema["testes"][1]["numero"] = 96

    response_problema, token_autor_problema = create_problema_user_helper(
        json_problema)
    problema_id = response_problema.json().get("data").get("id")

    problema_teste = JSON_PROBLEMA_TESTE.copy()
    problema_teste["problema_id"] = problema_id
    problema_teste["numero"] = 100

    response_problema_teste = client.post(
        URL_PROBLEMA_TESTE,
        json=problema_teste,
        headers={
            "Authorization": f"Bearer {token_autor_problema}",
        },
    )

    id_problema_teste = response_problema_teste.json().get("data").get("id")

    response = client.patch(
        f"{URL_PROBLEMA_TESTE}/{id_problema_teste}/",
        json={
            "numero": 96
        },
        headers={
            "Authorization": f"Bearer {token_autor_problema}",
        },
    )

    assert response.status_code == 400

    resume_dependencies()


def test_update_full_problema_teste():
    remove_dependencies()

    json_problema = JSON_PROBLEMA.copy()
    json_problema["testes"][0]["numero"] = 1
    json_problema["testes"][1]["numero"] = 2

    response_problema, token_autor_problema = create_problema_user_helper(
        json_problema)
    problema_id = response_problema.json().get("data").get("id")

    problema_teste = JSON_PROBLEMA_TESTE.copy()
    problema_teste["problema_id"] = problema_id
    problema_teste["numero"] = 100

    response_problema_teste = client.post(
        URL_PROBLEMA_TESTE,
        json=problema_teste,
        headers={
            "Authorization": f"Bearer {token_autor_problema}",
        },
    )

    id_problema_teste = response_problema_teste.json().get("data").get("id")

    response = client.put(
        f"{URL_PROBLEMA_TESTE}/{id_problema_teste}/",
        json={
            "numero": 100,
            "tipo": "gerado",
            "exemplo": False,
            "entrada": "Newstring",
            "descricao": "Newstring",
            "problema_id": problema_id
        },
        headers={
            "Authorization": f"Bearer {token_autor_problema}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


JSON_PROBLEMA_TESTE = {
    "numero": 100,
    "tipo": "manual",
    "exemplo": True,
    "entrada": "string",
    "descricao": "string",
    "problema_id": 0
}
