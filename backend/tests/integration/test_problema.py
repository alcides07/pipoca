from backend.main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)

URL_PROBLEMA = "/problemas"
JSON_PROBLEMA = {
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
            ],
    "arquivos": [
                {
                    "nome": "string",
                    "corpo": "string",
                    "secao": "recursos"
                }
            ],
    "verificador": {
                "nome": "string",
                "linguagem": "string",
                "corpo": "string"
            },
    "validador": {
                "nome": "string",
                "linguagem": "string",
                "corpo": "string"
            }
}


def test_read_problema_unit():
    remove_dependencies()

    response = client.post(
        URL_PROBLEMA,
        json=JSON_PROBLEMA
    )

    problema_id = response.json().get("data", {}).get("id", None)
    response = client.get(f"{URL_PROBLEMA}/{problema_id}/")
    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas():
    remove_dependencies()

    response = client.get(
        URL_PROBLEMA,
    )
    assert response.status_code == 200

    resume_dependencies()


def test_create_problema():
    remove_dependencies()

    response = client.post(
        URL_PROBLEMA,
        json=JSON_PROBLEMA
    )
    assert response.status_code == 201

    resume_dependencies()
