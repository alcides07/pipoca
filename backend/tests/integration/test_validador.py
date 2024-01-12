from backend.main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)
URL_VALIDADOR = "/validadores"


def test_read_validadores():
    remove_dependencies()

    response = client.get(
        URL_VALIDADOR
    )
    assert response.status_code == 200

    resume_dependencies()
