from schemas.common.compilers import CompilersEnum
from tests.database import get_db_test
from tests.helpers.administrador import create_administrador_helper
from tests.helpers.problema_resposta import JSON_PROBLEMA_RESPOSTA, URL_PROBLEMA_RESPOSTAS, create_problema_resposta_helper
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
        path_problema="./tests/integration/example_problem.zip",
        resposta=JSON_PROBLEMA_RESPOSTA["resposta"],
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
        path_problema="./tests/integration/example_problem.zip",
        resposta=JSON_PROBLEMA_RESPOSTA["resposta"],
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
        path_problema="./tests/integration/example_problem.zip",
        resposta=JSON_PROBLEMA_RESPOSTA["resposta"],
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


def test_read_meus_problemas_respostas_com_user():
    remove_dependencies()

    response_user, token, _ = create_user_helper()
    user_id = response_user.json().get("data").get("id")

    response = client.get(
        f"{URL_PROBLEMA_RESPOSTAS}/usuarios/{user_id}/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 200

    resume_dependencies()


def test_read_meus_problemas_respostas_para_problema_especifico():
    remove_dependencies()

    _, token_user_criador_problema, _ = create_user_helper()
    response_usuario, token_user_resposta, _ = create_user_helper()
    id_usuario = response_usuario.json().get("data").get("id")

    response_problema = create_problema_resposta_helper(
        token_user_criador_problema=token_user_criador_problema,
        token_user_resposta=token_user_resposta,
        problema_privado=False,
        path_problema="./tests/integration/example_problem.zip",
        resposta=JSON_PROBLEMA_RESPOSTA["resposta"],
        linguagem=CompilersEnum("cpp.g++17")
    )
    assert response_problema.status_code == 201

    id_problema = response_problema.json().get("data").get("problema_id")

    response = client.get(
        f"{URL_PROBLEMA_RESPOSTAS}/problemas/{id_problema}/usuarios/{id_usuario}/",
        headers={
            "Authorization": f"Bearer {token_user_resposta}",
        },
    )

    assert response.status_code == 200
    assert len(response.json().get("data")) == 1

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
        path_problema="./tests/integration/example_problem.zip",
        resposta=JSON_PROBLEMA_RESPOSTA["resposta"],
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

    JSON_RESPOSTA = JSON_PROBLEMA_RESPOSTA.copy()
    JSON_RESPOSTA["resposta"] = "#include <iostream>\r\n#include <vector>\r\n#include <algorithm>\r\n \r\nusing namespace std;\r\n \r\npair<int, int> solve(vector<pair<int, int>>& v, int s) {\r\n    int left = 0, right = v.size() - 1;\r\n    while (left < right) {\r\n        int sum = v[left].first + v[right].first;\r\n        if (sum == s) return { v[left].second,v[right].second };\r\n        if (sum < s) left++;\r\n        else right--;\r\n    }\r\n    return { -1, -1 };\r\n}\r\n \r\nint main() {\r\n    int n, s; cin >> n >> s;\r\n    vector<pair<int, int>> v(n);\r\n    for (int i = 0; i < n; ++i) {\r\n        cin >> v[i].first;\r\n        v[i].second = i + 1;\r\n    }\r\n    sort(v.begin(), v.end());\r\n    auto ans = solve(v, s);\r\n    if (ans.first != -1)\r\n        cout << ans.first << \" \" << ans.second << endl;\r\n    else\r\n        cout < \"IMPOSSIVEL\\n\";\r\n    return 0;\r\n}\r\n"

    response = create_problema_resposta_helper(
        token_user_criador_problema=token_user_criador_problema,
        token_user_resposta=token_user_resposta,
        problema_privado=False,
        path_problema="./tests/integration/example_problem.zip",
        resposta=JSON_RESPOSTA["resposta"],
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
        path_problema="./tests/integration/example_problem.zip",
        resposta=JSON_PROBLEMA_RESPOSTA["resposta"],
        linguagem=CompilersEnum("cpp.g++17")
    )

    assert response.status_code == 401

    resume_dependencies()
