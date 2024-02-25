from tests.config_test import remove_dependencies
from fastapi.testclient import TestClient
from main import app
from tests.helpers.user import create_user_helper

client = TestClient(app)
URL_TAG = "/tags"


def create_only_tag_helper():
    remove_dependencies()

    tag = JSON_TAG.copy()
    _, token, _ = create_user_helper()

    response = client.post(
        URL_TAG,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=tag
    )

    return response, token


def create_tag_in_problema_helper(token: str, problema_id: int):
    remove_dependencies()

    tag = JSON_TAG.copy()

    response = client.post(
        URL_TAG,
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "nome": tag["nome"],
            "problema_id": problema_id
        }
    )

    return response


JSON_TAG = {
    "nome": "string"
}
