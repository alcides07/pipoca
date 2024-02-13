from tests.config_test import remove_dependencies
from fastapi.testclient import TestClient
from tests.helpers.problema import create_problema_admin_helper, create_problema_user_helper
from backend.main import app

client = TestClient(app)
URL_ARQUIVO = "/arquivos"


def create_arquivo_helper(profile: str = ""):
    remove_dependencies()

    if (profile == "admin"):
        response_problema_, token = create_problema_admin_helper()

    else:
        response_problema_, token = create_problema_user_helper()

    problema_id = response_problema_.json().get("data").get("id")

    arquivo = JSON_ARQUIVO.copy()
    arquivo["problema_id"] = problema_id

    response = client.post(
        URL_ARQUIVO,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=arquivo
    )

    return response, token


def update_partial_arquivo_helper(profile: str = ""):
    remove_dependencies()

    if (profile == "admin"):
        response_arquivo, token = create_arquivo_helper("admin")

    else:
        response_arquivo, token = create_arquivo_helper()

    arquivo = response_arquivo.json().get("data")
    arquivo_id = arquivo.get("id")

    json_partial = {
        "corpo": "novoCorpo"
    }

    response = client.patch(
        f"{URL_ARQUIVO}/{arquivo_id}/",
        json=json_partial,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    return response, arquivo


def update_full_arquivo_helper(profile: str = ""):
    remove_dependencies()

    if (profile == "admin"):
        response_arquivo, token = create_arquivo_helper("admin")

    else:
        response_arquivo, token = create_arquivo_helper()

    arquivo = response_arquivo.json().get("data")
    arquivo_id = arquivo.get("id")

    arquivo_copy = arquivo.copy()

    arquivo["nome"] = "PUT"
    arquivo["secao"] = "anexo"
    arquivo["status"] = "PUT"
    arquivo["corpo"] = "PUT"
    arquivo["problema_id"] = arquivo.get("problema_id")

    response = client.put(
        f"{URL_ARQUIVO}/{arquivo_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=arquivo
    )

    return response, arquivo_copy


JSON_ARQUIVO = {
    "nome": "string",
    "secao": "recursos",
    "status": "string",
    "corpo": "string",
    "problema_id": 0
}
