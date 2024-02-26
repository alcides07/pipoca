from tests.config_test import remove_dependencies
from fastapi.testclient import TestClient
from tests.helpers.problema import create_problema_admin_helper, create_problema_user_helper
from main import app

client = TestClient(app)
URL_VERIFICADOR = "/verificadores"


def create_verificador_helper(profile: str = ""):
    remove_dependencies()

    if (profile == "admin"):
        response_problema_, token = create_problema_admin_helper()

    else:
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


def update_partial_verificador_helper(profile: str = ""):
    remove_dependencies()

    if (profile == "admin"):
        response_verificador, token = create_verificador_helper("admin")

    else:
        response_verificador, token = create_verificador_helper()

    verificador = response_verificador.json().get("data")
    verificador_id = verificador.get("id")

    json_partial = {
        "corpo": "novoCorpo"
    }

    response = client.patch(
        f"{URL_VERIFICADOR}/{verificador_id}/",
        json=json_partial,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    return response, verificador


def update_full_verificador_helper(profile: str = ""):
    remove_dependencies()

    if (profile == "admin"):
        response_verificador, token = create_verificador_helper("admin")

    else:
        response_verificador, token = create_verificador_helper()

    verificador = response_verificador.json().get("data")
    verificador_id = verificador.get("id")

    verificador_copy = verificador.copy()

    verificador["nome"] = "PUT"
    verificador["linguagem"] = "PUT"
    verificador["corpo"] = "PUT"

    response = client.put(
        f"{URL_VERIFICADOR}/{verificador_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=verificador
    )

    return response, verificador_copy


JSON_VERIFICADOR = {
    "nome": "string",
    "linguagem": "string",
    "corpo": "string",
    "problema_id": 0
}
