from tests.config_test import remove_dependencies
from fastapi.testclient import TestClient
from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.user import create_user_helper
from main import app

client = TestClient(app)
URL_PROBLEMA = "/problemas"


def create_problema_user_helper(json_problema: dict = {}):
    remove_dependencies()

    problema = json_problema
    if (not json_problema):
        problema = JSON_PROBLEMA.copy()

    _, token, _ = create_user_helper()

    response = client.post(
        URL_PROBLEMA,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=problema
    )

    return response, token


def update_partial_problema_helper(profile: str = ""):
    remove_dependencies()

    response_problema, token = create_problema_user_helper()
    problema = response_problema.json().get("data")
    problema_id = problema.get("id")

    if (profile == "admin"):
        response_problema, token = create_problema_admin_helper()
        problema = response_problema.json().get("data")
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

    return response, problema


def update_full_problema_helper(profile: str = ""):
    remove_dependencies()

    response_problema, token = create_problema_user_helper()
    problema = response_problema.json().get("data")
    problema_id = problema.get("id")

    if (profile == "admin"):
        response_problema, token = create_problema_admin_helper()
        problema = response_problema.json().get("data")
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

    return response, problema_copy


def update_full_problema_fail_incomplete(profile: str = ""):
    remove_dependencies()

    response_problema, token = create_problema_user_helper()

    if (profile == "admin"):
        response_problema, token = create_problema_admin_helper()

    problema_id = response_problema.json().get("data").get("id")

    json_full_fake = {
        "nome": "nome",
    }

    response = client.put(
        f"{URL_PROBLEMA}/{problema_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=json_full_fake
    )

    return response


def create_problema_admin_helper(json_problema: dict = {}):
    remove_dependencies()

    problema = json_problema
    if (not json_problema):
        problema = JSON_PROBLEMA.copy()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response_admin = client.post(
        URL_PROBLEMA,
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
        json=problema
    )

    return response_admin, token_admin


JSON_PROBLEMA = {
    "nome": "string",
    "privado": True,
    "nome_arquivo_entrada": "string",
    "nome_arquivo_saida": "string",
    "tempo_limite": 250,
    "memoria_limite": 600,
    "declaracoes": [
                {
                    "titulo": "string",
                    "contextualizacao": "string",
                    "formatacao_entrada": "string",
                    "formatacao_saida": "string",
                    "observacao": "string",
                    "tutorial": "string",
                    "idioma": "Africâner"
                }
    ],
    "arquivos": [
        {
            "nome": "string",
                    "corpo": "string",
                    "secao": "recursos"
        }
    ],
    "verificador": {
        "nome": "string",
                "linguagem": "string",
                "corpo": "string",
        "testes": [
            {
                "numero": 1,
                "entrada": "string",
                "veredito": "ok"
            }
        ]
    },
    "validador": {
        "nome": "string",
                "linguagem": "string",
                "corpo": "string",
        "testes": [
            {
                "numero": 1,
                "entrada": "string",
                "veredito": "valid"

            },
            {
                "numero": 2,
                "entrada": "string",
                "veredito": "invalid"
            },
        ]
    },
    "tags": ["1", "2"],
    "testes": [
        {
            "numero": 1,
            "tipo": "manual",
            "exemplo": True,
            "entrada": "string",
            "descricao": "string"
        },
        {
            "numero": 2,
            "tipo": "gerado",
            "exemplo": False,
            "entrada": "string"
        }
    ],
}
