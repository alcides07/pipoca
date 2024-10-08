from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.problema import URL_PROBLEMA, create_problema_admin_helper, create_problema_user_helper
from tests.helpers.user import create_user_helper
from main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)
URL_DECLARACAO = "/declaracoes"


# -------------------------------
# Testes de leitura (GET)
# -------------------------------
def test_read_declaracao_all_com_user():
    remove_dependencies()

    _, token_user, _ = create_user_helper()

    response = client.get(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_declaracao_all_com_admin():
    remove_dependencies()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.get(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_declaracao_by_id_com_user_criador_do_problema():
    remove_dependencies()

    response_problema_user, token = create_problema_user_helper()
    problema_id = response_problema_user.json().get("data").get("id")

    declaracao = JSON_DECLARACAO.copy()
    declaracao["problema_id"] = problema_id

    response_declaracao = client.post(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=declaracao
    )
    declaracao_id = response_declaracao.json().get("data").get("id")

    response = client.get(
        f"{URL_DECLARACAO}/{declaracao_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_declaracao_by_id_com_user_nao_criador_do_problema():
    remove_dependencies()

    response_problema_user, token = create_problema_user_helper()
    problema_id = response_problema_user.json().get("data").get("id")

    declaracao = JSON_DECLARACAO.copy()
    declaracao["problema_id"] = problema_id

    response_declaracao = client.post(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=declaracao
    )
    declaracao_id = response_declaracao.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_DECLARACAO}/{declaracao_id}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_declaracao_by_id_com_admin():
    remove_dependencies()

    response_problema_user, token = create_problema_user_helper()
    problema_id = response_problema_user.json().get("data").get("id")

    declaracao = JSON_DECLARACAO.copy()
    declaracao["problema_id"] = problema_id

    response_declaracao = client.post(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=declaracao
    )
    declaracao_id = response_declaracao.json().get("data").get("id")

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.get(
        f"{URL_DECLARACAO}/{declaracao_id}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_idiomas_declaracao():
    remove_dependencies()

    _, token, _ = create_user_helper()

    response = client.get(
        f"{URL_DECLARACAO}/idiomas/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json().get("data") != []

    resume_dependencies()


def test_read_declaracao_imagens():
    remove_dependencies()

    _, token, _ = create_user_helper()

    with open("./tests/integration/example_problem_with_image.zip", 'rb') as file:
        response_problema = client.post(
            f"{URL_PROBLEMA}/pacotes/",
            files={"pacote": file},
            data={
                "privado": "true",
                "linguagens": ["python.3", "cpp.g++17"]
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert response_problema.status_code == 201

    id_problema = response_problema.json().get("data").get("id")

    response_declaracoes = client.get(
        f"{URL_PROBLEMA}/{id_problema}/declaracoes/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response_declaracoes.status_code == 200

    id_declaracao = response_declaracoes.json().get("data")[0].get("id")

    response = client.get(
        f"{URL_DECLARACAO}/{id_declaracao}/imagens/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json().get("data") != []

    resume_dependencies()


# -------------------------------
# Testes de escrita (POST)
# -------------------------------
def test_create_declaracao_com_user_criador_do_problema():
    remove_dependencies()

    response_problema_user, token = create_problema_user_helper()
    problema_id = response_problema_user.json().get("data").get("id")

    declaracao = JSON_DECLARACAO.copy()
    declaracao["problema_id"] = problema_id

    response = client.post(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=declaracao
    )

    assert response.status_code == 201

    resume_dependencies()


def test_create_declaracao_com_admin():
    remove_dependencies()

    response_problema_user, token_admin = create_problema_admin_helper()
    problema_id = response_problema_user.json().get("data").get("id")

    declaracao = JSON_DECLARACAO.copy()
    declaracao["problema_id"] = problema_id

    response = client.post(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
        json=declaracao
    )

    assert response.status_code == 201

    resume_dependencies()


# -------------------------------
# Testes de atualização parcial (PATCH)
# -------------------------------
def test_update_partial_declaracao_com_user_criador_do_problema():
    remove_dependencies()

    response_problema_user, token = create_problema_user_helper()
    problema_id = response_problema_user.json().get("data").get("id")

    declaracao = JSON_DECLARACAO.copy()
    declaracao["problema_id"] = problema_id

    response_declaracao = client.post(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=declaracao
    )
    declaracao_id = response_declaracao.json().get("data").get("id")

    json_declaracao = JSON_DECLARACAO.copy()
    json_declaracao["titulo"] = "NovoTitulo"
    json_declaracao["tutorial"] = "NovoTutorial"
    json_declaracao["contextualizacao"] = "NovaContextualizacao"

    response = client.patch(
        f"{URL_DECLARACAO}/{declaracao_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_declaracao
    )

    assert response.status_code == 200

    resume_dependencies()


def test_update_partial_declaracao_com_user_nao_criador_do_problema():
    remove_dependencies()

    response_problema_user, token = create_problema_user_helper()
    problema_id = response_problema_user.json().get("data").get("id")

    declaracao = JSON_DECLARACAO.copy()
    declaracao["problema_id"] = problema_id

    response_declaracao = client.post(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=declaracao
    )
    declaracao_id = response_declaracao.json().get("data").get("id")

    json_declaracao = JSON_DECLARACAO.copy()
    json_declaracao["titulo"] = "NovoTitulo"
    json_declaracao["tutorial"] = "NovoTutorial"
    json_declaracao["contextualizacao"] = "NovaContextualizacao"

    _, token_user, _ = create_user_helper()

    response = client.patch(
        f"{URL_DECLARACAO}/{declaracao_id}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
        json=json_declaracao
    )

    assert response.status_code == 401

    resume_dependencies()


# -------------------------------
# Testes de atualização total (PUT)
# -------------------------------
def test_update_total_declaracao_com_user_criador_do_problema():
    remove_dependencies()

    response_problema_user, token = create_problema_user_helper()
    problema_id = response_problema_user.json().get("data").get("id")

    declaracao = JSON_DECLARACAO.copy()
    declaracao["problema_id"] = problema_id

    response_declaracao = client.post(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=declaracao
    )
    declaracao_id = response_declaracao.json().get("data").get("id")

    json_declaracao = JSON_DECLARACAO.copy()
    json_declaracao["titulo"] = "NovoTitulo"
    json_declaracao["tutorial"] = "NovoTutorial"
    json_declaracao["contextualizacao"] = "NovaContextualizacao"
    json_declaracao["idioma"] = "Português"
    json_declaracao["formatacao_entrada"] = "nova_formatacao_entrada"
    json_declaracao["formatacao_saida"] = "nova_formatacao_saida"
    json_declaracao["observacao"] = "NovaObservacao"

    response = client.put(
        f"{URL_DECLARACAO}/{declaracao_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_declaracao
    )

    assert response.status_code == 200

    resume_dependencies()


def test_update_total_declaracao_com_user_nao_criador_do_problema():
    remove_dependencies()

    response_problema_user, token = create_problema_user_helper()
    problema_id = response_problema_user.json().get("data").get("id")

    declaracao = JSON_DECLARACAO.copy()
    declaracao["problema_id"] = problema_id

    response_declaracao = client.post(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=declaracao
    )
    declaracao_id = response_declaracao.json().get("data").get("id")

    json_declaracao = JSON_DECLARACAO.copy()
    json_declaracao["titulo"] = "NovoTitulo"
    json_declaracao["tutorial"] = "NovoTutorial"
    json_declaracao["contextualizacao"] = "NovaContextualizacao"
    json_declaracao["idioma"] = "Português"
    json_declaracao["formatacao_entrada"] = "nova_formatacao_entrada"
    json_declaracao["formatacao_saida"] = "nova_formatacao_saida"
    json_declaracao["observacao"] = "NovaObservacao"

    _, token_user, _ = create_user_helper()

    response = client.put(
        f"{URL_DECLARACAO}/{declaracao_id}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
        json=json_declaracao
    )

    assert response.status_code == 401

    resume_dependencies()


# -------------------------------
# Testes de exclusão (DELETE)
# -------------------------------
def test_delete_declaracao_com_user_criador_do_problema():
    remove_dependencies()

    response_problema_user, token = create_problema_user_helper()
    problema_id = response_problema_user.json().get("data").get("id")

    declaracao = JSON_DECLARACAO.copy()
    declaracao["problema_id"] = problema_id

    response_declaracao = client.post(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=declaracao
    )
    declaracao_id = response_declaracao.json().get("data").get("id")

    response = client.delete(
        f"{URL_DECLARACAO}/{declaracao_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 204

    resume_dependencies()


def test_delete_declaracao_com_user_nao_criador_do_problema():
    remove_dependencies()

    response_problema_user, token = create_problema_user_helper()
    problema_id = response_problema_user.json().get("data").get("id")

    declaracao = JSON_DECLARACAO.copy()
    declaracao["problema_id"] = problema_id

    response_declaracao = client.post(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=declaracao
    )
    declaracao_id = response_declaracao.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.delete(
        f"{URL_DECLARACAO}/{declaracao_id}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_delete_declaracao_com_admin():
    remove_dependencies()

    response_problema_user, token = create_problema_user_helper()
    problema_id = response_problema_user.json().get("data").get("id")

    declaracao = JSON_DECLARACAO.copy()
    declaracao["problema_id"] = problema_id

    response_declaracao = client.post(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=declaracao
    )
    declaracao_id = response_declaracao.json().get("data").get("id")

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.delete(
        f"{URL_DECLARACAO}/{declaracao_id}/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response.status_code == 204

    resume_dependencies()


JSON_DECLARACAO = {
    "titulo": "string",
    "idioma": "Português",
    "contextualizacao": "string",
    "formatacao_entrada": "string",
    "formatacao_saida": "string",
    "observacao": "string",
    "tutorial": "string",
    "problema_id": 0
}
