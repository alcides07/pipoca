from passlib.context import CryptContext
from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.problema import JSON_PROBLEMA, URL_PROBLEMA, create_problema_admin_helper, create_problema_user_helper, update_full_problema_fail_incomplete, update_full_problema_helper, update_partial_problema_helper
from tests.helpers.user import create_user_helper
from main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_read_problema_unit_user():
    remove_dependencies()

    response_problema_user, token = create_problema_user_helper()

    problema_id = response_problema_user.json().get("data").get("id")
    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problema_unit_admin():
    remove_dependencies()

    response_problema_admin, token = create_problema_admin_helper()

    problema_id = response_problema_admin.json().get("data").get("id")
    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas_user():
    remove_dependencies()

    _, token_user, _ = create_user_helper()

    response_problema_user = client.get(
        URL_PROBLEMA,
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )
    assert response_problema_user.status_code == 200

    resume_dependencies()


def test_read_meus_problemas_user():
    remove_dependencies()

    _, token_user, _ = create_user_helper()

    response_problema_user = client.get(
        f"{URL_PROBLEMA}/users/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )
    assert response_problema_user.status_code == 200

    resume_dependencies()


def test_read_problemas_admin():
    remove_dependencies()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response_problema_admin = client.get(
        URL_PROBLEMA,
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response_problema_admin.status_code == 200

    resume_dependencies()


def test_read_problemas_respostas_de_autor_by_problema_id_user():
    remove_dependencies()

    response_problema_criado, token_criador_problema = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/respostas/",
        headers={
            "Authorization": f"Bearer {token_criador_problema}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas_respostas_de_admin_by_problema_id_user():
    remove_dependencies()

    response_problema_criado, _ = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    database = next(get_db_test())
    token_adm = create_administrador_helper(database)

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/respostas/",
        headers={
            "Authorization": f"Bearer {token_adm}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas_respostas_de_naoautor_by_problema_id_user():
    remove_dependencies()

    response_problema_criado, _ = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/respostas/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_problemas_arquivos_de_autor_by_problema_id_user():
    remove_dependencies()

    response_problema_criado, token_criador_problema = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/arquivos/",
        headers={
            "Authorization": f"Bearer {token_criador_problema}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas_arquivos_de_nao_autor_by_problema_id_user():
    remove_dependencies()

    response_problema_criado, _ = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/arquivos/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_problemas_validador_de_autor_by_problema_id_user():
    remove_dependencies()

    response_problema_criado, token_criador_problema = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/validadores/",
        headers={
            "Authorization": f"Bearer {token_criador_problema}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas_validador_de_nao_autor_by_problema_id_user():
    remove_dependencies()

    response_problema_criado, _ = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/validadores/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_problemas_verificador_de_autor_by_problema_id_user():
    remove_dependencies()

    response_problema_criado, token_criador_problema = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/verificadores/",
        headers={
            "Authorization": f"Bearer {token_criador_problema}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas_verificador_de_nao_autor_by_problema_id_user():
    remove_dependencies()

    response_problema_criado, _ = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/verificadores/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_problemas_tags_de_autor_by_problema_id_user():
    remove_dependencies()

    response_problema_criado, token_criador_problema = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/tags/",
        headers={
            "Authorization": f"Bearer {token_criador_problema}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas_tags_de_nao_autor_by_problema_id_privado_user():
    remove_dependencies()

    json_problema = JSON_PROBLEMA.copy()
    json_problema["privado"] = True

    response_problema_criado, _ = create_problema_user_helper(json_problema)
    problema_id = response_problema_criado.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/tags/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_problemas_testes_de_autor_by_problema_id_user():
    remove_dependencies()

    response_problema_criado, token_criador_problema = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/testes/",
        headers={
            "Authorization": f"Bearer {token_criador_problema}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas_testes_de_nao_autor_by_problema_id_privado_user():
    remove_dependencies()

    json_problema = JSON_PROBLEMA.copy()
    json_problema["privado"] = True

    response_problema_criado, _ = create_problema_user_helper(json_problema)
    problema_id = response_problema_criado.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/testes/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_problemas_testes_nao_exemplos_de_nao_autor_by_problema_id_publico_user():
    remove_dependencies()

    json_problema = JSON_PROBLEMA.copy()
    json_problema["privado"] = False

    response_problema_criado, _ = create_problema_user_helper(json_problema)
    problema_id = response_problema_criado.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/testes/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
        params={"exemplo": False}
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_problemas_testes_exemplos_de_nao_autor_by_problema_id_publico_user():
    remove_dependencies()

    json_problema = JSON_PROBLEMA.copy()
    json_problema["privado"] = False

    response_problema_criado, _ = create_problema_user_helper(json_problema)
    problema_id = response_problema_criado.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/testes/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
        params={"exemplo": True}
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas_testes_de_nao_autor_by_problema_id_publico_user():
    remove_dependencies()

    json_problema = JSON_PROBLEMA.copy()
    json_problema["privado"] = False

    response_problema_criado, _ = create_problema_user_helper(json_problema)
    problema_id = response_problema_criado.json().get("data").get("id")

    _, token_user, _ = create_user_helper()

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/testes/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problemas_testes_de_admin_by_problema_id_user():
    remove_dependencies()

    response_problema_criado, _ = create_problema_user_helper()
    problema_id = response_problema_criado.json().get("data").get("id")

    database = next(get_db_test())
    token_adm = create_administrador_helper(database)

    response = client.get(
        f"{URL_PROBLEMA}/{problema_id}/testes/",
        headers={
            "Authorization": f"Bearer {token_adm}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_create_problema_user():
    remove_dependencies()

    response_problema_user, _ = create_problema_user_helper()

    assert response_problema_user.status_code == 201

    resume_dependencies()


def test_create_problema_user_nome_repetido():
    remove_dependencies()

    response_problema_original_user, _ = create_problema_user_helper()
    response_problema_repetido_user, _ = create_problema_user_helper()

    nome_problema_original = response_problema_original_user.json().get("data").get("nome")
    nome_problema_repetido = response_problema_repetido_user.json().get("data").get("nome")

    assert nome_problema_original != nome_problema_repetido

    resume_dependencies()


def test_create_problema_admin():
    remove_dependencies()

    response_problema_admin, _ = create_problema_admin_helper()

    assert response_problema_admin.status_code == 201

    resume_dependencies()


def test_update_partial_problema_user():
    remove_dependencies()

    response_problema_user, problema = update_partial_problema_helper()

    assert response_problema_user.status_code == 200

    response_json = response_problema_user.json().get("data")

    assert response_json.get(
        "nome") != problema.get("nome")

    assert response_json.get(
        "tempo_limite") == problema.get("tempo_limite")

    resume_dependencies()


def test_update_partial_problema_admin():
    remove_dependencies()

    response_problema_admin, problema = update_partial_problema_helper("admin")

    assert response_problema_admin.status_code == 200

    response_json = response_problema_admin.json().get("data")

    assert response_json.get(
        "nome") != problema.get("nome")

    assert response_json.get(
        "tempo_limite") == problema.get("tempo_limite")

    resume_dependencies()


def test_update_full_problema_user():
    remove_dependencies()

    response_problema_user, problema = update_full_problema_helper()
    assert response_problema_user.status_code == 200

    response_json = response_problema_user.json().get("data")

    assert response_json.get("nome") != problema.get("nome")

    assert response_json.get(
        "nome_arquivo_entrada") != problema.get("nome_arquivo_entrada")

    assert response_json.get(
        "nome_arquivo_saida") != problema.get("nome_arquivo_saida")

    assert response_json.get(
        "tempo_limite") == problema.get("tempo_limite")

    assert response_json.get(
        "memoria_limite") == problema.get("memoria_limite")

    resume_dependencies()


def test_update_full_problema_admin():
    remove_dependencies()

    response_problema_user, problema = update_full_problema_helper(
        "admin")
    assert response_problema_user.status_code == 200

    response_json = response_problema_user.json().get("data")

    assert response_json.get("nome") != problema.get("nome")

    assert response_json.get(
        "nome_arquivo_entrada") != problema.get("nome_arquivo_entrada")

    assert response_json.get(
        "nome_arquivo_saida") != problema.get("nome_arquivo_saida")

    assert response_json.get(
        "tempo_limite") == problema.get("tempo_limite")

    assert response_json.get(
        "memoria_limite") == problema.get("memoria_limite")

    resume_dependencies()


def test_update_full_problema_fail_user():
    remove_dependencies()

    response = update_full_problema_fail_incomplete()

    assert response.status_code == 422

    resume_dependencies()


def test_update_full_problema_fail_admin():
    remove_dependencies()

    response = update_full_problema_fail_incomplete("admin")

    assert response.status_code == 422

    resume_dependencies()


def test_upload_problema_user():
    remove_dependencies()

    _, token, _ = create_user_helper()

    with open("./tests/integration/example_problem", 'rb') as file:
        response = client.post(
            f"{URL_PROBLEMA}/upload/",
            files={"pacote": file},
            data={"privado": "true"},
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert response.status_code == 201

    resume_dependencies()


def test_upload_problema_admin():
    remove_dependencies()

    database = next(get_db_test())
    token = create_administrador_helper(database)

    with open("./tests/integration/example_problem", 'rb') as file:
        response = client.post(
            f"{URL_PROBLEMA}/upload/",
            files={"pacote": file},
            data={"privado": "true"},
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    assert response.status_code == 201

    resume_dependencies()
