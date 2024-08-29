import io
import os
import tarfile
import tempfile
import docker
from typing import List
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from constants import FILENAME_RUN, INPUT_TEST_FILENAME, OUTPUT_JUDGE_FILENAME, OUTPUT_USER_FILENAME
from dependencies.authorization_user import is_admin
from models.arquivo import Arquivo
from models.problemaResposta import ProblemaResposta
from models.user import User
from schemas.arquivo import SecaoEnum
from schemas.problemaResposta import ProblemaRespostaCreate
from schemas.problemaTeste import TipoTesteProblemaEnum
from utils.get_testlib import get_test_lib
from fastapi import status
from docker.errors import DockerException
from compilers import commands
from models.problema import Problema
from workers.celery import app
from sqlalchemy.orm import configure_mappers
from database import SessionLocal
from workers.celeryconfig import correcao_problema_queue

configure_mappers()


@app.task(
    bind=True,
    queue=correcao_problema_queue.name,
    autoretry_for=(Exception,),
    retry_backoff=True,
    time_limit=600
)
def correcao_problema(
    self,
    problema_resposta_dict: dict,
    user_id: int,
    problema_id: int
):
    def get_arquivo_gerador(db_problema: Problema):
        for arquivo in db_problema.arquivos:
            if (arquivo.secao == SecaoEnum.GERADOR.value):
                return arquivo
        return None

    def execute_checker(
        db_problema: Problema,
        output_codigo_solucao: list[str],
        output_codigo_user: list[str]
    ):
        codigo_verificador = db_problema.verificador.corpo
        linguagem_verificador: str = db_problema.verificador.linguagem
        extensao_verificador: str = commands[linguagem_verificador]["extension"]
        veredito: list[str] = []

        client = docker.from_env()
        image = commands[linguagem_verificador]["image"]
        WORKING_DIR = "/checker/testes/"

        client.images.pull(image)
        volume = client.volumes.create()
        command = commands[linguagem_verificador]["run_checker"]

        volumes = {
            volume.name: {  # type: ignore
                'bind': WORKING_DIR,
                'mode': 'rw'
            }
        }

        with tempfile.NamedTemporaryFile(delete=False) as temp_testlib:
            response = get_test_lib()
            temp_testlib.write(response.encode())
            TEMP_TESTLIB = temp_testlib.name

        with tempfile.NamedTemporaryFile(delete=False) as temp_codigo_verificador:
            temp_codigo_verificador.write(codigo_verificador.encode())
            TEMP_CODIGO_VERIFICADOR = temp_codigo_verificador.name

        try:
            for i, teste in enumerate(db_problema.testes):
                teste_entrada = teste.entrada

                if (teste.tipo == TipoTesteProblemaEnum.GERADO.value):
                    teste_entrada = teste.entrada_gerado

                try:
                    container = client.containers.create(
                        image,
                        command,
                        detach=True,
                        volumes=volumes,
                        working_dir=WORKING_DIR
                    )

                    with tempfile.NamedTemporaryFile(delete=False) as temp_teste_problema:
                        temp_teste_problema.write(teste_entrada.encode())
                        TEMP_TESTE_PROBLEMA = temp_teste_problema.name

                    with tempfile.NamedTemporaryFile(delete=False) as temp_saida_usuario:
                        temp_saida_usuario.write(
                            output_codigo_user[i].encode())
                        TEMP_SAIDA_USUARIO = temp_saida_usuario.name

                    with tempfile.NamedTemporaryFile(delete=False) as temp_saida_juiz:
                        temp_saida_juiz.write(
                            output_codigo_solucao[i].encode())
                        TEMP_SAIDA_JUIZ = temp_saida_juiz.name

                    tarstream = io.BytesIO()
                    tar = tarfile.TarFile(fileobj=tarstream, mode='w')

                    tar.add(
                        name=TEMP_TESTLIB,
                        arcname=f'{WORKING_DIR}/testlib.h'
                    )
                    tar.add(
                        name=TEMP_SAIDA_JUIZ,
                        arcname=f'{WORKING_DIR}/{OUTPUT_JUDGE_FILENAME}'
                    )
                    tar.add(
                        name=TEMP_SAIDA_USUARIO,
                        arcname=f'{WORKING_DIR}/{OUTPUT_USER_FILENAME}'
                    )
                    tar.add(
                        name=TEMP_CODIGO_VERIFICADOR,
                        arcname=f'{WORKING_DIR}/{FILENAME_RUN}{extensao_verificador}'
                    )
                    tar.add(
                        name=TEMP_TESTE_PROBLEMA,
                        arcname=f'{WORKING_DIR}/{INPUT_TEST_FILENAME}'
                    )

                    tar.close()

                    container.put_archive(  # type: ignore
                        '/',
                        tarstream.getvalue()
                    )

                    container.start()  # type: ignore
                    container.wait()  # type: ignore

                    stderr_logs = container.logs(
                        stdout=False, stderr=True).decode()  # type: ignore

                    if (stderr_logs != ""):
                        veredito_mensagem = stderr_logs.split()
                        veredito.append(veredito_mensagem[0].lower())

                except DockerException:
                    raise HTTPException(
                        status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "Ocorreu um erro no processo de comparação dos resultados!"
                    )

                finally:
                    container.stop()  # type: ignore
                    container.remove()  # type: ignore
                    os.remove(TEMP_TESTE_PROBLEMA)
                    os.remove(TEMP_SAIDA_USUARIO)
                    os.remove(TEMP_SAIDA_JUIZ)

        finally:
            os.remove(TEMP_CODIGO_VERIFICADOR)
            os.remove(TEMP_TESTLIB)
            volume.remove()  # type: ignore

        return veredito

    def get_saidas_testes(db_problema: Problema) -> list[str]:
        return [teste.saida for teste in db_problema.testes]

    def execute_codigo_user(
        db_problema: Problema,
        problema_resposta: ProblemaRespostaCreate,
        arquivo_gerador: Arquivo | None
    ):
        codigo_user = problema_resposta.resposta
        linguagem = problema_resposta.linguagem
        extension = commands[linguagem.value]["extension"]

        client = docker.from_env()
        image = commands[linguagem.value]["image"]
        WORKING_DIR = "/user/submission/"

        client.images.pull(image)
        volume = client.volumes.create()
        command = commands[linguagem]["run_test"]

        volumes = {
            volume.name: {  # type: ignore
                'bind': WORKING_DIR,
                'mode': 'rw'
            }
        }

        with tempfile.NamedTemporaryFile(delete=False) as temp_codigo_usuario:
            temp_codigo_usuario.write(codigo_user.encode())
            TEMP_CODIGO_USUARIO = temp_codigo_usuario.name

        output_codigo_user: List[str] = []

        try:
            for i, teste in enumerate(db_problema.testes):
                teste_entrada = teste.entrada

                if (teste.tipo == TipoTesteProblemaEnum.GERADO.value):
                    if (arquivo_gerador is None):
                        raise HTTPException(
                            status.HTTP_500_INTERNAL_SERVER_ERROR,
                            "O arquivo gerador de testes não foi encontrado!"
                        )

                    teste_entrada = teste.entrada_gerado

                try:
                    container = client.containers.create(
                        image=image,
                        command=command,
                        detach=True,
                        volumes=volumes,
                        working_dir=WORKING_DIR
                    )

                    with tempfile.NamedTemporaryFile(delete=False) as temp_teste_problema:
                        temp_teste_problema.write(teste_entrada.encode())
                        TEMP_TESTE_PROBLEMA = temp_teste_problema.name

                    tarstream = io.BytesIO()
                    tar = tarfile.TarFile(fileobj=tarstream, mode='w')

                    tar.add(
                        name=TEMP_CODIGO_USUARIO,
                        arcname=f'{WORKING_DIR}/{FILENAME_RUN}{extension}'
                    )
                    tar.add(
                        name=TEMP_TESTE_PROBLEMA,
                        arcname=f'{WORKING_DIR}/{INPUT_TEST_FILENAME}'
                    )

                    tar.close()

                    container.put_archive(  # type: ignore
                        '/',
                        tarstream.getvalue()
                    )

                    container.start()  # type: ignore
                    container.wait()  # type: ignore

                    stdout_logs = container.logs(
                        stdout=True, stderr=False).decode()  # type: ignore
                    stderr_logs = container.logs(
                        stdout=False, stderr=True).decode()  # type: ignore

                    output_codigo_user.append(stdout_logs)

                    if (stderr_logs != ""):
                        return f"Erro em tempo de execução no teste {i+1}"

                except DockerException:
                    raise HTTPException(
                        status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "Ocorreu um erro no processamento do código do usuário!"
                    )

                finally:
                    container.stop()  # type: ignore
                    container.remove()  # type: ignore
                    os.remove(TEMP_TESTE_PROBLEMA)

        finally:
            os.remove(TEMP_CODIGO_USUARIO)
            volume.remove()  # type: ignore

        return output_codigo_user

    def execute_processo_resolucao(
        problema_resposta: ProblemaRespostaCreate,
        db_problema: Problema
    ):
        arquivo_gerador = get_arquivo_gerador(db_problema)

        output_codigo_user = execute_codigo_user(
            db_problema,
            problema_resposta,
            arquivo_gerador
        )

        if (isinstance(output_codigo_user, str)):
            return [], [], [], output_codigo_user

        output_codigo_solucao = get_saidas_testes(
            db_problema,
        )

        veredito = execute_checker(
            db_problema,
            output_codigo_solucao,
            output_codigo_user
        )

        return veredito, output_codigo_user, output_codigo_solucao, None

    try:
        db = SessionLocal()
        db_user = db.query(User).filter(User.id == user_id).first()
        db_problema = db.query(Problema).filter(
            Problema.id == problema_id).first()

        problema_resposta = ProblemaRespostaCreate(**problema_resposta_dict)

        veredito, output_user, output_judge, erro = execute_processo_resolucao(
            problema_resposta=problema_resposta,
            db_problema=db_problema
        )

        db_problema_resposta = ProblemaResposta(**problema_resposta_dict)
        db_problema_resposta.veredito = veredito  # type: ignore
        db_problema_resposta.erro = erro  # type: ignore
        db_problema_resposta.saida_usuario = output_user  # type: ignore
        db_problema_resposta.saida_esperada = output_judge  # type: ignore
        db_problema_resposta.usuario = db_user

        # Bloco temporário
        db_problema_resposta.tempo = 250   # type: ignore
        db_problema_resposta.memoria = 250  # type: ignore
        #

        db_problema.respostas.append(db_problema_resposta)

        if (is_admin(db_user)):
            db_problema_resposta.usuario = None

        db.add(db_problema_resposta)
        db.commit()
        db.refresh(db_problema_resposta)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ocorreu um erro na criação da resposta para o problema!"
        )

    return jsonable_encoder(db_problema_resposta)
