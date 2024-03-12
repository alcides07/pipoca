from schemas.common.compilers import CompilersEnum
from tests.config_test import remove_dependencies
from fastapi.testclient import TestClient
from tests.helpers.problema import URL_PROBLEMA
from main import app

client = TestClient(app)
URL_PROBLEMA_RESPOSTAS = "/problemaRespostas"


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
            f"{URL_PROBLEMA}/upload/",
            files={"pacote": file},
            data={"privado": str(problema_privado)},
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
    "resposta": "string",
    "linguagem": "python.3",
    "problema_id": 0
}
