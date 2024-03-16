from schemas.common.compilers import CompilersEnum
from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.problema_resposta import URL_PROBLEMA_RESPOSTAS, create_problema_resposta_helper
from tests.helpers.user import create_user_helper
from main import app
from fastapi.testclient import TestClient
from tests.config_test import remove_dependencies, resume_dependencies

client = TestClient(app)


# -------------------------------
# Testes de leitura (GET)
# -------------------------------
def test_read_problema_respostas_all_com_user():
    remove_dependencies()

    _, token, _ = create_user_helper()

    response = client.get(
        URL_PROBLEMA_RESPOSTAS,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 401

    resume_dependencies()


def test_read_problema_respostas_all_com_admin():
    remove_dependencies()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.get(
        URL_PROBLEMA_RESPOSTAS,
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )
    assert response.status_code == 200

    resume_dependencies()


def test_read_problema_resposta_by_id_com_user_criador_do_problema():
    remove_dependencies()

    _, token_user, _ = create_user_helper()

    response_problema_resposta = create_problema_resposta_helper(
        token_user_criador_problema=token_user,
        token_user_resposta=token_user,
        problema_privado=False,
        path_problema="./tests/integration/multiplication_problem.zip",
        resposta="#include<iostream>\nusing namespace std;\nint main() {\nint a, b;\ncin >> a >> b;\ncout << a * b;\nreturn 0;\n}",
        linguagem=CompilersEnum("cpp.g++17")
    )

    response_resposta_id = response_problema_resposta.json().get("data").get("id")

    response = client.get(
        f"{URL_PROBLEMA_RESPOSTAS}/{response_resposta_id}/",
        headers={
            "Authorization": f"Bearer {token_user}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problema_resposta_by_id_com_user_autor_da_resposta():
    remove_dependencies()

    _, token_user_criador_problema, _ = create_user_helper()
    _, token_user_resposta, _ = create_user_helper()

    response_problema_resposta = create_problema_resposta_helper(
        token_user_criador_problema=token_user_criador_problema,
        token_user_resposta=token_user_resposta,
        problema_privado=False,
        path_problema="./tests/integration/multiplication_problem.zip",
        resposta="#include<iostream>\nusing namespace std;\nint main() {\nint a, b;\ncin >> a >> b;\ncout << a * b;\nreturn 0;\n}",
        linguagem=CompilersEnum("cpp.g++17")
    )

    response_resposta_id = response_problema_resposta.json().get("data").get("id")

    response = client.get(
        f"{URL_PROBLEMA_RESPOSTAS}/{response_resposta_id}/",
        headers={
            "Authorization": f"Bearer {token_user_resposta}",
        },
    )

    assert response.status_code == 200

    resume_dependencies()


def test_read_problema_resposta_by_id_com_user_qualquer_negado():
    remove_dependencies()

    _, token_user_criador_problema, _ = create_user_helper()
    _, token_user_resposta, _ = create_user_helper()
    _, token_user_qualquer, _ = create_user_helper()

    response_problema_resposta = create_problema_resposta_helper(
        token_user_criador_problema=token_user_criador_problema,
        token_user_resposta=token_user_resposta,
        problema_privado=False,
        path_problema="./tests/integration/multiplication_problem.zip",
        resposta="#include<iostream>\nusing namespace std;\nint main() {\nint a, b;\ncin >> a >> b;\ncout << a * b;\nreturn 0;\n}",
        linguagem=CompilersEnum("cpp.g++17")
    )

    response_resposta_id = response_problema_resposta.json().get("data").get("id")

    response = client.get(
        f"{URL_PROBLEMA_RESPOSTAS}/{response_resposta_id}/",
        headers={
            "Authorization": f"Bearer {token_user_qualquer}",
        },
    )

    assert response.status_code == 401

    resume_dependencies()


def test_read_meus_problema_respostas_com_user():
    remove_dependencies()

    _, token, _ = create_user_helper()

    response = client.get(
        f"{URL_PROBLEMA_RESPOSTAS}/users/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 200

    resume_dependencies()


def test_read_meus_problema_respostas_com_admin():
    remove_dependencies()

    database = next(get_db_test())
    token_admin = create_administrador_helper(database)

    response = client.get(
        f"{URL_PROBLEMA_RESPOSTAS}/users/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )
    assert response.status_code == 200

    resume_dependencies()


# -------------------------------
# Testes de escrita (POST)
# -------------------------------
def test_create_problema_resposta_com_user_qualquer():
    remove_dependencies()

    _, token_user_criador_problema, _ = create_user_helper()
    _, token_user_resposta, _ = create_user_helper()

    response = create_problema_resposta_helper(
        token_user_criador_problema=token_user_criador_problema,
        token_user_resposta=token_user_resposta,
        problema_privado=False,
        path_problema="./tests/integration/multiplication_problem.zip",
        resposta="#include<iostream>\nusing namespace std;\nint main() {\nint a, b;\ncin >> a >> b;\ncout << a * b;\nreturn 0;\n}",
        linguagem=CompilersEnum("cpp.g++17")
    )
    response_json = response.json().get("data")
    erro = response_json.get("erro")
    veredito = response_json.get("veredito")
    saida_usuario = response_json.get("saida_usuario")
    saida_esperada = response_json.get("saida_esperada")

    assert erro == None
    assert veredito != []
    assert saida_usuario != []
    assert saida_esperada != []
    assert response.status_code == 201

    resume_dependencies()


def test_create_problema_resposta_runtime_error_com_user_qualquer():
    remove_dependencies()

    _, token_user_criador_problema, _ = create_user_helper()
    _, token_user_resposta, _ = create_user_helper()

    response = create_problema_resposta_helper(
        token_user_criador_problema=token_user_criador_problema,
        token_user_resposta=token_user_resposta,
        problema_privado=False,
        path_problema="./tests/integration/multiplication_problem.zip",
        resposta="#include<iostream>\nusingg namespace std;\nint main() {\nint a, b;\ncin >> a >> b;\ncout << a * b;\nreturn 0;\n}",
        linguagem=CompilersEnum("cpp.g++17")
    )
    erro = response.json().get("data").get("erro")

    assert erro != None
    assert response.status_code == 201

    resume_dependencies()


def test_create_problema_resposta_de_problema_privado_com_user_qualquer():
    remove_dependencies()

    _, token_user_criador_problema, _ = create_user_helper()
    _, token_user_resposta, _ = create_user_helper()

    response = create_problema_resposta_helper(
        token_user_criador_problema=token_user_criador_problema,
        token_user_resposta=token_user_resposta,
        problema_privado=True,
        path_problema="./tests/integration/multiplication_problem.zip",
        resposta="#include<iostream>\nusing namespace std;\nint main() {\nint a, b;\ncin >> a >> b;\ncout << a * b;\nreturn 0;\n}",
        linguagem=CompilersEnum("cpp.g++17")
    )

    assert response.status_code == 401

    resume_dependencies()
