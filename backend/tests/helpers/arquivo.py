from tests.config_test import remove_dependencies
from fastapi.testclient import TestClient
from tests.helpers.problema import create_problema_admin_helper, create_problema_user_helper
from backend.main import app

client = TestClient(app)
URL_ARQUIVO = "/arquivos"


def create_arquivo_user_helper():
    remove_dependencies()

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


def create_arquivo_admin_helper():
    remove_dependencies()

    response_problema, token = create_problema_admin_helper()
    problema_id = response_problema.json().get("data").get("id")

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


JSON_ARQUIVO = {
    "nome": "string",
    "secao": "recursos",
    "status": "string",
    "corpo": "string",
    "problema_id": 0
}
