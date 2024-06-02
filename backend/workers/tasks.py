import asyncio
import io
import os
import tarfile
import tempfile
import docker
from typing import List
from fastapi import HTTPException
from constants import FILENAME_RUN, INPUT_TEST_FILENAME, OUTPUT_JUDGE_FILENAME, OUTPUT_USER_FILENAME
from dependencies.database import get_session_local
from models.arquivo import Arquivo
from models.problema import Problema
from models.problemaTeste import ProblemaTeste
from schemas.arquivo import SecaoEnum
from schemas.problemaResposta import ProblemaRespostaCreate
from schemas.problemaTeste import TipoTesteProblemaEnum
from utils.get_testlib import get_test_lib
from workers.celery import app
from fastapi import status
from docker.errors import DockerException
from compilers import commands


@app.task(bind=True,
          queue="correcao-problema",
          autoretry_for=(Exception,),
          retry_backoff=True
          )
def correcao_problema(
    self,
    problema_resposta: ProblemaRespostaCreate,
    db_problema: dict
):
    db_problema = Problema(**db_problema)
    loop = asyncio.get_event_loop()

    def get_arquivo_solucao(
        db_problema: Problema
    ):
        for arquivo in db_problema.arquivos:
            if (arquivo.secao == SecaoEnum.SOLUCAO.value and arquivo.status == "main"):
                return arquivo

        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "O arquivo de solução principal do problema não foi encontrado!"
        )

    def get_arquivo_gerador(db_problema: Problema):
        for arquivo in db_problema.arquivos:
            if (arquivo.secao == SecaoEnum.GERADOR.value):
                return arquivo
        return None

    async def execute_checker(
        db_problema: Problema,
        output_codigo_solucao: list[str],
        output_codigo_user: list[str],
        output_testes_gerados: List[str]
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
                    teste_entrada = output_testes_gerados[i]

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

                    stderr_logs = container.logs(  # type: ignore
                        stdout=False, stderr=True).decode()

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

    async def execute_teste_gerado(
        teste: ProblemaTeste,
        arquivo_gerador: Arquivo
    ):
        linguagem_gerador: str = arquivo_gerador.linguagem  # type: ignore
        extensao_gerador: str = commands[linguagem_gerador]["extension"]

        client = docker.from_env()
        image = commands[linguagem_gerador]["image"]
        WORKING_DIR = "/problema/gerador/"

        teste_entrada = " ".join(teste.entrada.split()[1:])
        client.images.pull(image)
        volume = client.volumes.create()
        command = commands[linguagem_gerador]["run_gerador"]

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

        with tempfile.NamedTemporaryFile(delete=False) as temp_codigo_gerador:
            temp_codigo_gerador.write(arquivo_gerador.corpo.encode())
            TEMP_CODIGO_GERADOR = temp_codigo_gerador.name

        with tempfile.NamedTemporaryFile(delete=False) as temp_teste_problema:
            temp_teste_problema.write(teste_entrada.encode())
            TEMP_TESTE_PROBLEMA = temp_teste_problema.name

        try:
            container = client.containers.create(
                image,
                command,
                detach=True,
                volumes=volumes,
                working_dir=WORKING_DIR
            )

            tarstream = io.BytesIO()
            tar = tarfile.TarFile(fileobj=tarstream, mode='w')

            tar.add(
                name=TEMP_TESTLIB,
                arcname=f'{WORKING_DIR}/testlib.h'
            )
            tar.add(
                name=TEMP_TESTE_PROBLEMA,
                arcname=f'{WORKING_DIR}/{INPUT_TEST_FILENAME}'
            )
            tar.add(
                name=TEMP_CODIGO_GERADOR,
                arcname=f'{WORKING_DIR}/{FILENAME_RUN}{extensao_gerador}'
            )

            tar.close()

            container.put_archive(  # type: ignore
                '/',
                tarstream.getvalue()
            )

            container.start()  # type: ignore

            container.wait()  # type: ignore

            stdout_logs = container.logs(  # type: ignore
                stdout=True, stderr=False).decode()
            stderr_logs = container.logs(  # type: ignore
                stdout=False, stderr=True).decode()

            if (stderr_logs != ""):
                raise HTTPException(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "O arquivo gerador de testes do problema possui alguma falha!"
                )

        except DockerException:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro na execução dos testes gerados!"
            )

        finally:
            container.stop()  # type: ignore
            container.remove()  # type: ignore
            os.remove(TEMP_TESTLIB)
            os.remove(TEMP_CODIGO_GERADOR)
            os.remove(TEMP_TESTE_PROBLEMA)
            volume.remove()  # type: ignore

        return stdout_logs

    async def execute_arquivo_solucao(
        db_problema: Problema,
        arquivo_solucao: Arquivo,
        output_testes_gerados: List[str]
    ):
        codigo_solucao = str(arquivo_solucao.corpo)
        linguagem = str(arquivo_solucao.linguagem)
        extension = commands[linguagem]["extension"]

        client = docker.from_env()
        image = commands[linguagem]["image"]
        command = commands[linguagem]["run_test"]
        WORKING_DIR = "/arquivo/testes/"

        client.images.pull(image)
        volume = client.volumes.create()

        volumes = {
            volume.name: {  # type: ignore
                'bind': WORKING_DIR,
                'mode': 'rw'
            }
        }

        with tempfile.NamedTemporaryFile(delete=False) as temp_codigo_solucao:
            temp_codigo_solucao.write(codigo_solucao.encode())
            TEMP_CODIGO_SOLUCAO = temp_codigo_solucao.name

        output_codigo_solucao: List[str] = []

        try:
            for i, teste in enumerate(db_problema.testes):
                teste_entrada = teste.entrada

                if (teste.tipo == TipoTesteProblemaEnum.GERADO.value):
                    teste_entrada = output_testes_gerados[i]

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
                        name=TEMP_CODIGO_SOLUCAO,
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

                    stdout_logs = container.logs(  # type: ignore
                        stdout=True, stderr=False).decode()
                    stderr_logs = container.logs(  # type: ignore
                        stdout=False, stderr=True).decode()

                    output_codigo_solucao.append(stdout_logs)

                    if (stderr_logs != ""):
                        raise HTTPException(
                            status.HTTP_500_INTERNAL_SERVER_ERROR,
                            "O arquivo de solução oficial do problema possui alguma falha!"
                        )

                except DockerException:
                    raise HTTPException(
                        status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "Ocorreu um erro no processamento do arquivo de solução oficial do problema!"
                    )

                finally:
                    container.stop()  # type: ignore
                    container.remove()  # type: ignore
                    os.remove(TEMP_TESTE_PROBLEMA)

        finally:
            os.remove(TEMP_CODIGO_SOLUCAO)
            volume.remove()  # type: ignore

        return output_codigo_solucao

    async def execute_codigo_user(
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
        output_testes_gerados: List[str] = []

        try:
            for i, teste in enumerate(db_problema.testes):
                teste_entrada = teste.entrada

                if (teste.tipo == TipoTesteProblemaEnum.GERADO.value):
                    if (arquivo_gerador is None):
                        raise HTTPException(
                            status.HTTP_500_INTERNAL_SERVER_ERROR,
                            "O arquivo gerador de testes não foi encontrado!"
                        )

                    teste_entrada = await execute_teste_gerado(
                        teste, arquivo_gerador
                    )

                output_testes_gerados.append(teste_entrada)

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

                    stdout_logs = container.logs(  # type: ignore
                        stdout=True, stderr=False).decode()
                    stderr_logs = container.logs(  # type: ignore
                        stdout=False, stderr=True).decode()

                    output_codigo_user.append(stdout_logs)

                    if (stderr_logs != ""):
                        return f"Erro em tempo de execução no teste {i+1}", []

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

        return output_codigo_user, output_testes_gerados

    arquivo_solucao = get_arquivo_solucao(db_problema)
    arquivo_gerador = get_arquivo_gerador(db_problema)

    output_codigo_user, output_testes_gerados = loop.run_until_complete(
        execute_codigo_user(
            db_problema,
            problema_resposta,
            arquivo_gerador
        )
    )

    if (isinstance(output_codigo_user, str)):
        return [], [], [], output_codigo_user

    output_codigo_solucao = loop.run_until_complete(
        execute_arquivo_solucao(
            db_problema,
            arquivo_solucao,
            output_testes_gerados
        )
    )

    veredito = loop.run_until_complete(
        execute_checker(
            db_problema,
            output_codigo_solucao,
            output_codigo_user,
            output_testes_gerados
        )
    )

    return "oi"
