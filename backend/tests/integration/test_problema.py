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
                "corpo": "string",
        "testes": [
            {
                "codigo": "string",
                "entrada": "string"
            }
        ]
    },
    "tags": ["1", "2"]
}


def test_read_problema_unit():
    remove_dependencies()
    json = JSON_PROBLEMA.copy()

    response = client.post(
        URL_PROBLEMA,
        json=json
    )

    problema_id = response.json().get("data").get("id")
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
    json = JSON_PROBLEMA.copy()

    response = client.post(
        URL_PROBLEMA,
        json=json
    )
    assert response.status_code == 201

    resume_dependencies()


def test_update_partial_problema():
    remove_dependencies()
    json = JSON_PROBLEMA.copy()

    response_post = client.post(
        URL_PROBLEMA,
        json=json
    ).json().get("data")

    problema_id = response_post.get("id")

    json_partial = {
        "nome": "NovoNome",
        "tags": ["Tag1, Tag2"]
    }

    response_patch = client.patch(
        f"{URL_PROBLEMA}/{problema_id}/",
        json=json_partial
    )

    assert response_patch.status_code == 200

    response_patch_json = response_patch.json().get("data")

    assert response_patch_json.get(
        "nome") != response_post.get("nome")

    assert response_patch_json.get(
        "tags") != response_post.get("tags")

    assert response_patch_json.get(
        "tempo_limite") == response_post.get("tempo_limite")

    resume_dependencies()


def test_update_full_problema_success():
    remove_dependencies()
    json_full = JSON_PROBLEMA.copy()

    response_post = client.post(
        URL_PROBLEMA,
        json=json_full
    ).json().get("data")

    problema_id = response_post.get("id")

    json_full["nome"] = "PUT"
    json_full["nome_arquivo_entrada"] = "PUT"
    json_full["nome_arquivo_saida"] = "PUT"
    json_full.pop("tags")

    response_put = client.put(
        f"{URL_PROBLEMA}/{problema_id}/",
        json=json_full
    )

    assert response_put.status_code == 200

    response_put_json = response_put.json().get("data")

    assert response_put_json.get("nome") != response_post.get("nome")

    assert response_put_json.get(
        "nome_arquivo_entrada") != response_post.get("nome_arquivo_entrada")

    assert response_put_json.get(
        "nome_arquivo_saida") != response_post.get("nome_arquivo_saida")

    assert response_put_json.get(
        "tempo_limite") == response_post.get("tempo_limite")

    assert response_put_json.get(
        "memoria_limite") == response_post.get("memoria_limite")

    resume_dependencies()


def test_update_full_problema_fail():
    remove_dependencies()
    json = JSON_PROBLEMA.copy()

    response_post = client.post(
        URL_PROBLEMA,
        json=json
    ).json().get("data")

    problema_id = response_post.get("id")

    json_full_fake = {
        "nome": "nome",
    }

    response_put = client.put(
        f"{URL_PROBLEMA}/{problema_id}/",
        json=json_full_fake
    )

    assert response_put.status_code == 422


def test_upload_problema():
    remove_dependencies()

    with open("./tests/integration/upload_problem.zip", 'rb') as file:
        response = client.post(
            f"{URL_PROBLEMA}/upload/",
            files={"pacote": file},
        )

    assert response.status_code == 201

    resume_dependencies()
