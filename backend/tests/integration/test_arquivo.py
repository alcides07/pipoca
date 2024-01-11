from backend.main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)


def test_read_arquivos():
    remove_dependencies()

    response = client.get(
        "/arquivos",
    )
    assert response.status_code == 200

    resume_dependencies()
