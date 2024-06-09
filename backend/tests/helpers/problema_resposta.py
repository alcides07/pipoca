from schemas.common.compilers import CompilersEnum
from tests.config_test import remove_dependencies
from fastapi.testclient import TestClient
from tests.helpers.problema import URL_PROBLEMA
from main import app

client = TestClient(app)
URL_PROBLEMA_RESPOSTAS = "/problemasRespostas"


def create_problema_resposta_helper(
    token_user_criador_problema: str,
    token_user_resposta: str,
    problema_privado: bool,
    path_problema: str,
    resposta: str,
    linguagem: CompilersEnum
):
    remove_dependencies()

    with open(path_problema, 'rb') as file:
        response_problema = client.post(
            f"{URL_PROBLEMA}/pacotes/",
            files={"pacote": file},
            data={
                "privado": str(problema_privado),
                "linguagens": ["python.3", "cpp.g++17"]
            },
            headers={
                "Authorization": f"Bearer {token_user_criador_problema}",
            },
        )

        problema_id = response_problema.json().get("data").get("id")

        json_resposta = JSON_PROBLEMA_RESPOSTA.copy()
        json_resposta["problema_id"] = problema_id
        json_resposta["resposta"] = resposta
        json_resposta["linguagem"] = linguagem

        response = client.post(
            URL_PROBLEMA_RESPOSTAS,
            json=json_resposta,
            headers={
                "Authorization": f"Bearer {token_user_resposta}",
            },
        )

        return response


JSON_PROBLEMA_RESPOSTA = {
    "resposta": "#include <iostream>\r\n#include <vector>\r\n#include <algorithm>\r\n \r\nusing namespace std;\r\n \r\npair<int, int> solve(vector<pair<int, int>>& v, int s) {\r\n    int left = 0, right = v.size() - 1;\r\n    while (left < right) {\r\n        int sum = v[left].first + v[right].first;\r\n        if (sum == s) return { v[left].second,v[right].second };\r\n        if (sum < s) left++;\r\n        else right--;\r\n    }\r\n    return { -1, -1 };\r\n}\r\n \r\nint main() {\r\n    int n, s; cin >> n >> s;\r\n    vector<pair<int, int>> v(n);\r\n    for (int i = 0; i < n; ++i) {\r\n        cin >> v[i].first;\r\n        v[i].second = i + 1;\r\n    }\r\n    sort(v.begin(), v.end());\r\n    auto ans = solve(v, s);\r\n    if (ans.first != -1)\r\n        cout << ans.first << \" \" << ans.second << endl;\r\n    else\r\n        cout << \"IMPOSSIVEL\\n\";\r\n    return 0;\r\n}\r\n",
    "linguagem": "cpp.g++17",
    "problema_id": 0
}
