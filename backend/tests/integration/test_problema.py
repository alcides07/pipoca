from backend.main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)


def test_create_problema():
    remove_dependencies()

    response = client.post(
        "/problemas",
        json={
            "nome": "string",
            "nome_arquivo_entrada": "string",
            "nome_arquivo_saida": "string",
            "tempo_limite": 250,
            "memoria_limite": 600,
            "tags": [
                "string"
            ],
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
            ]
        }
    )
    assert response.status_code == 201

    resume_dependencies()
