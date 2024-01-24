from tests.config_test import remove_dependencies
from fastapi.testclient import TestClient
from tests.helpers.user import create_user_helper
from backend.main import app

client = TestClient(app)
URL_PROBLEMA = "/problemas"


def create_problema_helper():
    remove_dependencies()

    problema = JSON_PROBLEMA.copy()
    _, token = create_user_helper()

    response = client.post(
        URL_PROBLEMA,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "accept": "application/json"
        },
        json=problema
    )

    return response, token


JSON_PROBLEMA = {
    "nome": "string",
    "privado": True,
    "nome_arquivo_entrada": "string",
    "nome_arquivo_saida": "string",
    "tempo_limite": 250,
    "memoria_limite": 600,
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
                "corpo": "string",
        "testes": [
            {
                "numero": "string",
                "entrada": "string",
                "veredito": "ok"
            }
        ]
    },
    "validador": {
        "nome": "string",
                "linguagem": "string",
                "corpo": "string",
        "testes": [
            {
                "numero": "string",
                "entrada": "string",
                "veredito": "valid"

            },
            {
                "numero": "string",
                "entrada": "string",
                "veredito": "invalid"
            },
        ]
    },
    "tags": ["1", "2"],
}
