from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.problema import URL_PROBLEMA, create_problema_user_helper
from tests.helpers.problema import JSON_PROBLEMA
from tests.helpers.user import create_user_helper
from main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)
URL_PROBLEMA_RESPOSTA = "/problemaRespostas"


def test_read_problema_resposta_unit_privado_e_autor_do_problema_e_da_resposta_user():
    remove_dependencies()

    response_problema_criado, token_autor_problema = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    resposta_submissao = JSON_PROBLEMA_RESPOSTA.copy()
    resposta_submissao["problema_id"] = problema_id

    response_resposta = client.post(
        URL_PROBLEMA_RESPOSTA,
        json=resposta_submissao,
        headers={
            "Authorization": f"Bearer {token_autor_problema}",
        },
    )
    id_resposta = response_resposta.json().get("data").get("id")

    response = client.get(
        f"{URL_PROBLEMA_RESPOSTA}/{id_resposta}",
        headers={
            "Authorization": f"Bearer {token_autor_problema}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problema_resposta_unit_privado_nao_sou_autor_nem_respondi_user():
    remove_dependencies()

    response_problema_criado, token_criador = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    resposta_submissao = JSON_PROBLEMA_RESPOSTA.copy()
    resposta_submissao["problema_id"] = problema_id

    response_resposta = client.post(
        URL_PROBLEMA_RESPOSTA,
        json=resposta_submissao,
        headers={
            "Authorization": f"Bearer {token_criador}",
        },
    )
    id_resposta = response_resposta.json().get("data").get("id")

    _, token_user_verifica, _ = create_user_helper()

    response = client.get(
        f"{URL_PROBLEMA_RESPOSTA}/{id_resposta}",
        headers={
            "Authorization": f"Bearer {token_user_verifica}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_problema_resposta_unit_privado_nao_sou_autor_mas_respondi_user():
    remove_dependencies()
    json_problema = JSON_PROBLEMA.copy()
    json_problema["privado"] = False

    response_problema_criado, token_criador_problema = create_problema_user_helper(
        json_problema)
    problema_id = response_problema_criado.json().get("data").get("id")

    resposta_submissao = JSON_PROBLEMA_RESPOSTA.copy()
    resposta_submissao["problema_id"] = problema_id

    _, token_usuario_resposta, _ = create_user_helper()

    response_resposta = client.post(
        URL_PROBLEMA_RESPOSTA,
        json=resposta_submissao,
        headers={
            "Authorization": f"Bearer {token_usuario_resposta}",
        },
    )
    id_resposta = response_resposta.json().get("data").get("id")

    client.patch(
        f"{URL_PROBLEMA}/{problema_id}/",
        json={
            "privado": True
        },
        headers={
            "Authorization": f"Bearer {token_criador_problema}",
        },
    )

    response = client.get(
        f"{URL_PROBLEMA_RESPOSTA}/{id_resposta}",
        headers={
            "Authorization": f"Bearer {token_usuario_resposta}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problema_resposta_unit_publico_nao_sou_autor_mas_respondi_user():
    remove_dependencies()
    json_problema = JSON_PROBLEMA.copy()
    json_problema["privado"] = False

    response_problema_criado, _ = create_problema_user_helper(
        json_problema)
    problema_id = response_problema_criado.json().get("data").get("id")

    resposta_submissao = JSON_PROBLEMA_RESPOSTA.copy()
    resposta_submissao["problema_id"] = problema_id

    _, token_usuario_resposta, _ = create_user_helper()

    response_resposta = client.post(
        URL_PROBLEMA_RESPOSTA,
        json=resposta_submissao,
        headers={
            "Authorization": f"Bearer {token_usuario_resposta}",
        },
    )
    id_resposta = response_resposta.json().get("data").get("id")

    response = client.get(
        f"{URL_PROBLEMA_RESPOSTA}/{id_resposta}",
        headers={
            "Authorization": f"Bearer {token_usuario_resposta}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas_respostas_user():
    remove_dependencies()

    _, token_user, _ = create_user_helper()

    response = client.get(
        URL_PROBLEMA_RESPOSTA,
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )
    assert response.status_code == 401

    resume_dependencies()


def test_read_problemas_respostas_admin():
    remove_dependencies()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.get(
        URL_PROBLEMA_RESPOSTA,
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )
    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas_respostas_de_naoautor_by_problema_id_admin():
    remove_dependencies()

    response_problema_criado, _ = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/respostas/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_minhas_respostas_problemas():
    remove_dependencies()

    _, token_user, _ = create_user_helper()

    response_problema_user = client.get(
        f"{URL_PROBLEMA_RESPOSTA}/users/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )
    assert response_problema_user.status_code == 200

    resume_dependencies()


def test_create_problema_resposta_em_problema_privado_negado_user():
    remove_dependencies()

    response_problema_criado, _ = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    _, token_usuario_resposta, _ = create_user_helper()
    resposta_submissao = JSON_PROBLEMA_RESPOSTA.copy()
    resposta_submissao["problema_id"] = problema_id

    response = client.post(
        URL_PROBLEMA_RESPOSTA,
        json=resposta_submissao,
        headers={
            "Authorization": f"Bearer {token_usuario_resposta}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_create_problema_resposta_em_problema_privado_autor_permitido_user():
    remove_dependencies()

    response_problema_criado, token_autor_problema = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    resposta_submissao = JSON_PROBLEMA_RESPOSTA.copy()
    resposta_submissao["problema_id"] = problema_id

    response = client.post(
        URL_PROBLEMA_RESPOSTA,
        json=resposta_submissao,
        headers={
            "Authorization": f"Bearer {token_autor_problema}",
        },
    )

    assert response.status_code == 201

    resume_dependencies()


def test_create_problema_resposta_em_problema_privado_admin_permitido_user():
    remove_dependencies()

    response_problema_criado, _ = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    resposta_submissao = JSON_PROBLEMA_RESPOSTA.copy()
    resposta_submissao["problema_id"] = problema_id

    database = next(get_db_test())
    administrador_token = create_administrador_helper(database)

    response = client.post(
        URL_PROBLEMA_RESPOSTA,
        json=resposta_submissao,
        headers={
            "Authorization": f"Bearer {administrador_token}",
        },
    )

    assert response.status_code == 201

    resume_dependencies()


def test_create_problema_resposta_em_problema_publico_user():
    remove_dependencies()

    json_problema = JSON_PROBLEMA.copy()
    json_problema["privado"] = False

    response_problema_criado, _ = create_problema_user_helper(
        json_problema)
    problema_id = response_problema_criado.json().get("data").get("id")

    _, token_user_resposta, _ = create_user_helper()
    resposta_submissao = JSON_PROBLEMA_RESPOSTA.copy()
    resposta_submissao["problema_id"] = problema_id

    response = client.post(
        URL_PROBLEMA_RESPOSTA,
        json=resposta_submissao,
        headers={
            "Authorization": f"Bearer {token_user_resposta}",
        },
    )

    assert response.status_code == 201

    resume_dependencies()


def test_create_problema_resposta_em_problema_publico_admin():
    remove_dependencies()

    json_problema = JSON_PROBLEMA.copy()
    json_problema["privado"] = False

    response_problema_criado, _ = create_problema_user_helper(
        json_problema)
    problema_id = response_problema_criado.json().get("data").get("id")

    database = next(get_db_test())
    administrador_token = create_administrador_helper(database)

    resposta_submissao = JSON_PROBLEMA_RESPOSTA.copy()
    resposta_submissao["problema_id"] = problema_id

    response = client.post(
        URL_PROBLEMA_RESPOSTA,
        json=resposta_submissao,
        headers={
            "Authorization": f"Bearer {administrador_token}",
        },
    )

    assert response.status_code == 201

    resume_dependencies()


JSON_PROBLEMA_RESPOSTA = {
    "resposta": "string",
    "tempo": 0,
    "memoria": 0,
    "linguagem": "string",
    "problema_id": 0
}
