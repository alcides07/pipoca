from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.problema import create_problema_admin_helper, create_problema_user_helper
from tests.helpers.user import create_user_helper
from main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)
URL_DECLARACAO = "/declaracoes"


def test_read_declaracoes_user():
    _, token_user, _ = create_user_helper()

    response = client.get(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401


def test_read_declaracoes_admin():
    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.get(
        URL_DECLARACAO,
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response.status_code == 200


def test_read_declaracao_unit_dono_user():
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


def test_read_declaracao_unit_nao_dono_user():
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


def test_read_declaracao_unit_admin():
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


def test_create_declaracao_dono_user():
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


def test_create_declaracao_admin():
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


def test_update_partial_declaracao_dono_user():
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


def test_update_partial_declaracao_nao_dono_user():
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


def test_update_total_declaracao_dono_user():
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


def test_update_total_declaracao_nao_dono_user():
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


def test_delete_declaracao_dono_user():
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


def test_delete_declaracao_nao_dono_user():
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


def test_delete_declaracao_admin():
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


JSON_DECLARACAO = {
    "titulo": "string",
    "idioma": "Africâner",
    "contextualizacao": "string",
    "formatacao_entrada": "string",
    "formatacao_saida": "string",
    "observacao": "string",
    "tutorial": "string",
    "problema_id": 0
}
