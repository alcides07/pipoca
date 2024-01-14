from backend.main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)
URL_VERIFICADOR = "/verificadores"


def test_read_verificadores():
    remove_dependencies()

    response = client.get(
        URL_VERIFICADOR
    )
    assert response.status_code == 200

    resume_dependencies()
