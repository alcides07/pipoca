import docker
import os
import tempfile
from typing import List, Tuple
from dependencies.authenticated_user import get_authenticated_user
from dependencies.authorization_user import is_admin, is_user
from fastapi import HTTPException, status
from models.problemaResposta import ProblemaResposta
from schemas.arquivo import SecaoEnum
from schemas.problemaResposta import ProblemaRespostaCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.problema import Problema
from docker.errors import DockerException
from languages_run import FILENAME_RUN, INPUT_FILENAME, commands


def get_arquivo_solucao(
        db_problema: Problema
):
    for arquivo in db_problema.arquivos:
        if (arquivo.secao == SecaoEnum.SOLUCAO and arquivo.status == "main"):
            linguagem = os.path.splitext(arquivo.nome)[1]
            return arquivo, linguagem
    return None


def compare_solucao_e_submissao(
        output_codigo_solucao: list[Tuple[str, str]],
        output_codigo_user: list[Tuple[str, str]]
):
    i = 0
    veredito = ""

    for codigo_user in output_codigo_user:
        if (codigo_user[0] == output_codigo_solucao[i][0]):
            veredito += "ok\n"

        else:
            veredito += "wrong-answer\n"

        i += 1

    return veredito


def execute_arquivo_solucao(db_problema: Problema, arquivo_solucao: Tuple):
    arquivo = arquivo_solucao[0]
    linguagem = arquivo_solucao[1]
    codigo = arquivo.corpo
    output_testes: List[Tuple[str, str]] = []

    client = docker.from_env()
    image = commands[linguagem]["image"]
    command = commands[linguagem]["run"]

    with tempfile.TemporaryDirectory() as temp_dir:
        for teste in db_problema.testes:

            with open(os.path.join(temp_dir, f"{FILENAME_RUN}{linguagem}"), "w") as file:
                file.write(codigo)

            with open(os.path.join(temp_dir, INPUT_FILENAME), "w") as file:
                file.write(teste.entrada)
            try:
                client.images.pull(image)
                volumes = {temp_dir: {
                    'bind': '/arquivo/testes/', 'mode': 'rw'}}

                container = client.containers.run(
                    image,
                    command,
                    detach=True,
                    volumes=volumes,
                    working_dir='/arquivo/testes/'
                )

                container.wait()  # type: ignore

                stdout_logs = container.logs(  # type: ignore
                    stdout=True, stderr=False)
                stderr_logs = container.logs(  # type: ignore
                    stdout=False, stderr=True)

                stdout_logs_decode = stdout_logs.decode()
                stderr_logs_decode = stderr_logs.decode()

                output_testes.append((stdout_logs_decode, stderr_logs_decode))

                container.stop()  # type: ignore
                container.remove()  # type: ignore

                if (stderr_logs_decode != ""):
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            except DockerException:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return output_testes


def execute_user_code(
    db_problema: Problema,
    problema_resposta: ProblemaRespostaCreate
):
    codigo_user = problema_resposta.resposta
    codigo_user_linguagem = problema_resposta.linguagem
    client = docker.from_env()
    image = commands[codigo_user_linguagem]["image"]
    command = commands[codigo_user_linguagem]["run"]
    output_testes_user: List[Tuple[str, str]] = []

    with tempfile.TemporaryDirectory() as temp_dir:
        for i, teste in enumerate(db_problema.testes):

            with open(os.path.join(temp_dir, f"{FILENAME_RUN}{codigo_user_linguagem}"), "w") as file:
                file.write(codigo_user)

            with open(os.path.join(temp_dir, INPUT_FILENAME), "w") as file:
                file.write(teste.entrada)

            try:
                client.images.pull(image)
                volumes = {temp_dir: {
                    'bind': '/user/submission/', 'mode': 'rw'}}

                container = client.containers.run(
                    image,
                    command,
                    detach=True,
                    volumes=volumes,
                    working_dir='/user/submission/'
                )

                container.wait()  # type: ignore

                stdout_logs = container.logs(  # type: ignore
                    stdout=True, stderr=False)
                stderr_logs = container.logs(  # type: ignore
                    stdout=False, stderr=True)

                stdout_logs_decode = stdout_logs.decode()
                stderr_logs_decode = stderr_logs.decode()

                output_testes_user.append(
                    (stdout_logs_decode, stderr_logs_decode))

                container.stop()  # type: ignore
                container.remove()  # type: ignore

                if (stderr_logs_decode != ""):
                    return "error", f"Runtime error no teste {i+1}"

            except DockerException:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return output_testes_user


def execute_processo_resolucao(
    problema_resposta: ProblemaRespostaCreate,
    db_problema: Problema
):
    arquivo_solucao = get_arquivo_solucao(db_problema)
    if (arquivo_solucao):
        output_codigo_solucao = execute_arquivo_solucao(
            db_problema,
            arquivo_solucao
        )

        output_codigo_user = execute_user_code(
            db_problema,
            problema_resposta
        )

        print("Output arquivo solução: ", output_codigo_solucao)
        print("")
        print("Output testes user: ", output_codigo_user)

        if (isinstance(output_codigo_user, tuple) and output_codigo_user[0] == 'error'):
            return output_codigo_user

        veredito = compare_solucao_e_submissao(
            output_codigo_solucao,
            output_codigo_user
        )
        return veredito

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def create_problema_resposta(
    db: Session,
    problema_resposta: ProblemaRespostaCreate,
    token: str
):
    db_problema = db.query(Problema).filter(
        Problema.id == problema_resposta.problema_id
    ).first()

    if (not db_problema):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Problema não encontrado!")

    user = await get_authenticated_user(token, db)
    if (bool(db_problema.privado) == True):
        if (is_user(user) and bool(user.id != db_problema.usuario_id)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Erro. O problema o qual se está tentando submeter uma resposta é privado!")

    try:
        veredito = execute_processo_resolucao(
            problema_resposta=problema_resposta,
            db_problema=db_problema
        )

        db_problema_resposta = ProblemaResposta(
            **problema_resposta.model_dump(exclude=set(["problema", "usuario"])))

        db_problema.respostas.append(db_problema_resposta)

        db_problema_resposta.usuario = user

        db_problema_resposta.veredito = veredito  # type: ignore
        if (isinstance(veredito, tuple) and veredito[0] == 'error'):
            db_problema_resposta.veredito = veredito[1]  # type: ignore

        # Bloco temporário
        db_problema_resposta.tempo = 250
        db_problema_resposta.memoria = 250
        #

        if (is_admin(user)):
            db_problema_resposta.usuario = None

        db.add(db_problema_resposta)
        db.commit()
        db.refresh(db_problema_resposta)

        return db_problema_resposta

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def get_problema_resposta_by_id(
    db: Session,
    id: int,
    token: str
):
    db_problema_resposta = db.query(ProblemaResposta).filter(
        ProblemaResposta.id == id).first()

    if (not db_problema_resposta):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await get_authenticated_user(token, db)

    try:

        if (
            is_user(user)
            and
            db_problema_resposta.usuario_id != user.id  # Não sou o autor da resposta
            and
            db_problema_resposta.problema.usuario_id != user.id  # Não sou o autor do problema
        ):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return db_problema_resposta

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
