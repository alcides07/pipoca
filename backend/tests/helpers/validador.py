from tests.config_test import remove_dependencies
from fastapi.testclient import TestClient
from tests.helpers.problema import create_problema_admin_helper, create_problema_user_helper
from main import app


client = TestClient(app)
URL_VALIDADOR = "/validadores"


def create_validador_helper(profile: str = ""):
    remove_dependencies()

    if (profile == "admin"):
        response_problema_, token = create_problema_admin_helper()

    else:
        response_problema_, token = create_problema_user_helper()

    problema_id = response_problema_.json().get("data").get("id")

    validador = JSON_VALIDADOR.copy()
    validador["problema_id"] = problema_id

    response = client.post(
        URL_VALIDADOR,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=validador
    )

    return response, token


def update_partial_validador_helper(profile: str = ""):
    remove_dependencies()

    if (profile == "admin"):
        response_validador, token = create_validador_helper("admin")

    else:
        response_validador, token = create_validador_helper()

    validador = response_validador.json().get("data")
    validador_id = validador.get("id")

    json_partial = {
        "corpo": "novoCorpo"
    }

    response = client.patch(
        f"{URL_VALIDADOR}/{validador_id}/",
        json=json_partial,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    return response, validador


def update_full_validador_helper(profile: str = ""):
    remove_dependencies()

    if (profile == "admin"):
        response_validador, token = create_validador_helper("admin")

    else:
        response_validador, token = create_validador_helper()

    validador = response_validador.json().get("data")
    validador_id = validador.get("id")

    validador_copy = validador.copy()

    validador["nome"] = "PUT"
    validador["linguagem"] = "cpp.g++17"
    validador["corpo"] = "PUT"

    response = client.put(
        f"{URL_VALIDADOR}/{validador_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=validador
    )

    return response, validador_copy


JSON_VALIDADOR = {
    "nome": "string",
    "linguagem": "python.3",
    "corpo": "string",
    "problema_id": 0
}
