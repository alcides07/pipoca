from tests.config_test import remove_dependencies
from fastapi.testclient import TestClient
from tests.helpers.problema import create_problema_admin_helper, create_problema_user_helper
from backend.main import app

client = TestClient(app)
URL_VERIFICADOR = "/verificadores"


def create_verificador_user_helper():
    remove_dependencies()

    response_problema_, token = create_problema_user_helper()
    problema_id = response_problema_.json().get("data").get("id")

    verificador = JSON_VERIFICADOR.copy()
    verificador["problema_id"] = problema_id

    response = client.post(
        URL_VERIFICADOR,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=verificador
    )

    return response, token


def create_verificador_admin_helper():
    remove_dependencies()

    response_problema_, token = create_problema_admin_helper()
    problema_id = response_problema_.json().get("data").get("id")

    verificador = JSON_VERIFICADOR.copy()
    verificador["problema_id"] = problema_id

    response = client.post(
        URL_VERIFICADOR,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=verificador
    )

    return response, token


JSON_VERIFICADOR = {
    "nome": "string",
    "linguagem": "string",
    "corpo": "string",
    "problema_id": 0
}
