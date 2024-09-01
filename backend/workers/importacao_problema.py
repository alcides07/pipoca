import os
import json
import zipfile
import re
import xml.etree.ElementTree as ET
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from database import SessionLocal
from dependencies.authorization_user import is_admin
from models.arquivo import Arquivo
from models.problema import Problema
from models.user import User
from schemas.arquivo import ArquivoCreate, SecaoEnum
from schemas.declaracao import DeclaracaoCreate, DeclaracaoImagem
from schemas.problema import ProblemaCreateUpload
from schemas.problemaTeste import TipoTesteProblemaEnum
from fastapi import status
from workers.celery import app
from sqlalchemy.orm import configure_mappers
from workers.celeryconfig import importacao_problema_queue
from fastapi import HTTPException, status
from schemas.common.compilers import CompilersEnum
from schemas.declaracao import DeclaracaoCreate, DeclaracaoImagem
from schemas.idioma import IdiomaEnum
from schemas.problemaTeste import ProblemaTesteCreate, TipoTesteProblemaEnum
from schemas.validador import ValidadorCreate
from schemas.validadorTeste import ValidadorTesteCreate, VereditoValidadorTesteEnum
from schemas.verificador import VerificadorCreate
from schemas.verificadorTeste import VereditoVerificadorTesteEnum, VerificadorTesteCreate
from utils.bytes_to_megabytes import bytes_to_megabytes
from utils.get_values_from_enum import get_values_from_enum
from utils.language_parser import languages_parser
from schemas.problema import ProblemaCreateUpload
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


configure_mappers()


@app.task(
    bind=True,
    queue=importacao_problema_queue.name,
    autoretry_for=(Exception,),
    retry_backoff=True
)
def importacao_problema(
    self,
    problema_dict: dict,
    user_id: int,
    pacote_file_path: str
):

    problema = ProblemaCreateUpload(**problema_dict)

    def persist_saidas_testes(
        db: Session,
        db_problema: Problema
    ):
        try:
            from orm.problemaResposta import get_arquivo_gerador, get_arquivo_solucao

            arquivo_solucao = get_arquivo_solucao(db_problema)
            arquivo_gerador: Arquivo | None = get_arquivo_gerador(db_problema)

            for teste in db_problema.testes:
                teste_entrada = str(teste.entrada)

                if (bool(teste.tipo == TipoTesteProblemaEnum.GERADO.value)):
                    if (arquivo_gerador is None):
                        raise HTTPException(
                            status.HTTP_500_INTERNAL_SERVER_ERROR,
                            "O arquivo gerador de testes não foi encontrado!"
                        )

                    teste_entrada = execute_teste_gerado(
                        teste, arquivo_gerador
                    )

                    teste.entrada_gerado = teste_entrada

                saida_teste_executado = execute_arquivo_solucao_com_testes(
                    entrada=teste_entrada,
                    arquivo_solucao=arquivo_solucao
                )

                teste.saida = saida_teste_executado

            db.commit()
            db.refresh(db_problema)

        except SQLAlchemyError:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro na persistência das saídas dos testes do problema!"
            )

    def process_files_gerador(data: ET.Element, nome_arquivo_gerador: str):
        try:
            path_file = ""
            filename = ""

            for source in data.findall('.//files/executables/executable'):
                gerador = source.find("source")

                if (gerador != None):
                    path_file = gerador.get("path")

                    if (path_file != None):
                        fullname = os.path.basename(path_file)
                        filename, _ = os.path.splitext(fullname)

                        if (nome_arquivo_gerador in filename):
                            linguagem = gerador.get("type")
                            break

            if (path_file and fullname and linguagem):
                with zip.open(path_file) as file:
                    corpo = file.read().decode()

                if (linguagem not in CompilersEnum.__members__.values()):
                    linguagens_suportadas = get_values_from_enum(CompilersEnum)

                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST,
                        f"A linguagem de um dos arquivos geradores de testes é {linguagem}, que não é suportada no momento. As linguagens atualmente suportadas são: {linguagens_suportadas}"
                    )

                arquivo = ArquivoCreate(
                    nome=fullname, corpo=corpo, secao=SecaoEnum.GERADOR, linguagem=CompilersEnum(linguagem))

                problema.arquivos.append(arquivo)

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar o arquivo gerador de testes do problema!"
            )

    def process_files_recursos(data: ET.Element):
        try:
            for file in data.findall('.//resources/file'):
                path = file.get("path")

                if (path != None):
                    with zip.open(path) as file:
                        nome = file.name.split("/")[-1]
                        corpo = file.read().decode()

                        arquivo = ArquivoCreate(
                            nome=nome, corpo=corpo, secao=SecaoEnum.RECURSO, status=None)

                        problema.arquivos.append(arquivo)

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar os arquivos de recursos do problema!"
            )

    def process_files_solucao(data: ET.Element):
        try:
            for solution in data.findall('.//solutions/solution'):
                status_arquivo_solucao = str(solution.get("tag"))
                source = solution.find('source')

                if source != None:
                    path = source.get("path")
                    linguagem = source.get("type")

                if (path != None):
                    with zip.open(path) as file:
                        nome = file.name.split("/")[-1]
                        corpo = file.read().decode()

                    if (linguagem not in CompilersEnum.__members__.values()):
                        linguagens_suportadas = get_values_from_enum(
                            CompilersEnum)

                        raise HTTPException(
                            status.HTTP_400_BAD_REQUEST,
                            f"A linguagem de um dos arquivos de solução é {linguagem}, que não é suportada no momento. As linguagens atualmente suportadas são: {linguagens_suportadas}"
                        )

                    arquivo = ArquivoCreate(
                        nome=nome, corpo=corpo, linguagem=CompilersEnum(linguagem), secao=SecaoEnum.SOLUCAO, status=status_arquivo_solucao)

                    problema.arquivos.append(arquivo)

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar os arquivos de solução do problema!"
            )

    def process_tempo_limite(data: ET.Element):
        try:
            tempo_limite = data.find('.//time-limit')
            if tempo_limite != None and tempo_limite.text != None:
                problema.tempo_limite = int(tempo_limite.text)

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar o tempo limite do problema!"
            )

    def process_memoria_limite(data: ET.Element):
        try:
            memoria_limite = data.find('.//memory-limit')
            if memoria_limite != None and memoria_limite.text != None:
                memoria_converted = bytes_to_megabytes(int(
                    (memoria_limite.text)))

                problema.memoria_limite = memoria_converted

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar a memória limite do problema!"
            )

    def process_verificador(data: ET.Element):
        try:
            verificador = data.find('.//checker/source')
            if (verificador != None):
                path = verificador.get("path")
                linguagem = verificador.get("type")

                if path != None:
                    with zip.open(path) as file:
                        nome = os.path.basename(file.name)
                        corpo = file.read().decode()

                        if (linguagem not in CompilersEnum.__members__.values()):
                            linguagens_suportadas = get_values_from_enum(
                                CompilersEnum)

                            raise HTTPException(
                                status.HTTP_400_BAD_REQUEST,
                                f"A linguagem do verificador é {linguagem}, que não é suportada no momento. As linguagens atualmente suportadas são: {linguagens_suportadas}"
                            )

                        verificador = VerificadorCreate(
                            nome=nome, corpo=corpo, linguagem=CompilersEnum(linguagem), testes=[])

                        problema.verificador = verificador

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar o verificador do problema!"
            )

    def process_validador(data: ET.Element):
        try:
            validador = data.find(".//validator/source")
            if (validador != None):
                path = validador.get("path")
                linguagem = validador.get("type")

            if path != None:
                with zip.open(path) as file:
                    nome = os.path.basename(file.name)
                    corpo = file.read().decode()

                    if (linguagem not in CompilersEnum.__members__.values()):
                        linguagens_suportadas = get_values_from_enum(
                            CompilersEnum)

                        raise HTTPException(
                            status.HTTP_400_BAD_REQUEST,
                            f"A linguagem do validador é {linguagem}, que não é suportada no momento. As linguagens atualmente suportadas são: {linguagens_suportadas}"
                        )

                    validador = ValidadorCreate(
                        nome=nome, corpo=corpo, linguagem=CompilersEnum(linguagem), testes=[])

                    problema.validador = validador

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar o validador do problema!"
            )

    def process_verificador_teste(data: ET.Element):
        try:
            for indice, verificador_teste in enumerate(data.findall(".//checker/testset/tests/test"), start=1):
                verdict = verificador_teste.get("verdict")
                verdict_enum = VereditoVerificadorTesteEnum(verdict)

                verificador_teste = VerificadorTesteCreate(
                    numero=indice,
                    veredito=verdict_enum,
                    entrada=""
                )

                problema.verificador.testes.append(verificador_teste)

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar os testes do verificador do problema!"
            )

    def process_validador_teste(data):
        try:
            for indice, validador_teste in enumerate(data.findall(".//validator/testset/tests/test"), start=1):
                verdict = validador_teste.get("verdict")
                verdict_enum = VereditoValidadorTesteEnum(verdict)

                validador_teste = ValidadorTesteCreate(
                    numero=indice,
                    veredito=verdict_enum,
                    entrada=""
                )

                problema.validador.testes.append(validador_teste)

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar os testes do validador do problema!"
            )

    def process_name(data: ET.Element):
        try:
            if (data != None):
                problema.nome = str(data.get("short-name"))

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar o nome do problema!"
            )

    def process_tags(data: ET.Element):
        try:
            for tag in data.findall('.//tags/tag'):
                name = str(tag.get("value"))
                problema.tags.append(name)

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar as tags do problema!"
            )

    def process_tests(data: ET.Element):
        try:
            nome_arquivo_gerador = ""

            for indice, test in enumerate(data.findall(".//judging/testset/tests/test"), start=1):
                cmd = test.get("cmd")
                tipo = test.get("method")
                exemplo = test.get("sample")

                teste = ProblemaTesteCreate(
                    numero=indice, tipo=TipoTesteProblemaEnum.MANUAL, exemplo=False, entrada="")

                if (cmd != None):
                    nome_arquivo_gerador = cmd.split()[0]
                    teste.entrada = cmd

                if (tipo != None):
                    if (tipo == "manual"):
                        teste.tipo = TipoTesteProblemaEnum.MANUAL
                    elif (tipo == "generated"):
                        teste.tipo = TipoTesteProblemaEnum.GERADO

                if (exemplo != None):
                    if (exemplo == "true"):
                        teste.exemplo = True
                    elif (exemplo == "false"):
                        teste.exemplo = False

                problema.testes.append(teste)

            if (nome_arquivo_gerador != ""):
                process_files_gerador(data, nome_arquivo_gerador)

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar os testes do problema!"
            )

    def process_xml(zip, filename):
        with zip.open(filename) as xml:
            content = xml.read().decode()
            data = ET.fromstring(content)

            process_tempo_limite(data)

            process_memoria_limite(data)

            process_name(data)

            process_tests(data)

            process_tags(data)

            process_files_recursos(data)

            process_files_solucao(data)

            process_verificador(data)

            process_verificador_teste(data)

            process_validador(data)

            process_validador_teste(data)

    def process_declaracoes(zip, filename):
        try:
            with zip.open(filename) as statement:
                content = statement.read().decode()
                data = json.loads(content)

                nomes_imagens = re.findall(
                    r'\\includegraphics\[.*\]\{(.*?)\}', data["legend"]
                )

                declaracao = DeclaracaoCreate(
                    titulo=data["name"],
                    contextualizacao=data["legend"],
                    formatacao_entrada=data["input"],
                    formatacao_saida=data["output"],
                    tutorial=data["tutorial"],
                    observacao=data["notes"],
                    imagens=[],
                    idioma=IdiomaEnum[languages_parser.get(
                        data["language"].capitalize(), "OT")]
                )

                for nome_imagem in nomes_imagens:
                    partes_filename = filename.split('/')
                    endereco_statement = '/'.join(partes_filename[:-1])
                    caminho_imagem = os.path.join(
                        endereco_statement, nome_imagem
                    )

                    with zip.open(caminho_imagem) as file_imagem:
                        data = file_imagem.read()

                        declaracao_imagem = DeclaracaoImagem(
                            nome=nome_imagem,
                            conteudo=data
                        )

                        declaracao.imagens.append(declaracao_imagem)

                problema.declaracoes.append(declaracao)

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar as declarações do problema!"
            )

    def process_entrada_verificador_teste(zip: zipfile.ZipFile, directory: str):
        try:
            indice = 0

            for filename in zip.namelist():
                if filename != directory and filename.startswith(directory) and "." not in filename:
                    with zip.open(filename) as file:
                        content = file.read().decode()
                        verificador_teste = problema.verificador.testes[indice]
                        verificador_teste.entrada = content

                        indice += 1

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar as entradas dos testes do verificador do problema!"
            )

    def process_entrada_validador_teste(zip: zipfile.ZipFile, directory: str):
        try:
            indice = 0

            for filename in zip.namelist():
                if filename != directory and filename.startswith(directory):
                    with zip.open(filename) as file:
                        content = file.read().decode()

                        validador_teste = problema.validador.testes[indice]
                        validador_teste.entrada = content

                        indice += 1

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar as entradas dos testes do validador do problema!"
            )

    def process_entrada_teste_manual(zip: zipfile.ZipFile, directory: str):
        try:
            indice = 0

            for filename in zip.namelist():
                if (filename != directory and filename.startswith(directory)):
                    with zip.open(filename) as file:
                        content = file.read().decode()

                        teste = problema.testes[indice]
                        if (teste.tipo == TipoTesteProblemaEnum.MANUAL):
                            teste.entrada = content

                        indice += 1

        except Exception:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro ao processar as entradas dos testes manuais do problema!"
            )

    with zipfile.ZipFile(pacote_file_path, 'r') as zip:
        try:
            from orm.problema import create_arquivos, create_declaracoes, create_tags, create_testes, create_validador, create_validador_testes, create_verificador, create_verificador_testes, execute_arquivo_solucao_com_testes, execute_teste_gerado, get_unique_nome_problema, process_imagens_declaracoes

            for filename in zip.namelist():

                if filename.lower() == "problem.xml":
                    process_xml(zip, filename)

                    process_entrada_verificador_teste(
                        zip, "files/tests/checker-tests/"
                    )

                    process_entrada_validador_teste(
                        zip, "files/tests/validator-tests/"
                    )

                    process_entrada_teste_manual(
                        zip, "tests/"
                    )

                if filename.startswith("statements/") and filename.endswith("problem-properties.json"):
                    process_declaracoes(zip, filename)

            db = SessionLocal()
            db_user = db.query(User).filter(User.id == user_id).first()

            db_problema = Problema(
                **problema.model_dump(exclude=set(["tags", "declaracoes", "arquivos", "verificador", "validador", "usuario", "testes"])))
            db.add(db_problema)

            new_name_problema = get_unique_nome_problema(
                db=db, nome_problema=problema.nome)
            if (bool(new_name_problema)):
                db_problema.nome = new_name_problema

            for declaracao in problema.declaracoes:
                create_declaracoes(db, declaracao, db_problema)

            for arquivo in problema.arquivos:
                create_arquivos(db, arquivo, db_problema)

            for tag in problema.tags:
                create_tags(db, tag, db_problema)

            for teste in problema.testes:
                create_testes(db, teste, db_problema)

            create_verificador(db, problema, db_problema)
            create_verificador_testes(db, problema, db_problema)

            create_validador(db, problema, db_problema)
            create_validador_testes(db, problema, db_problema)

            db_problema.usuario = db_user

            if (is_admin(db_user)):
                db_problema.usuario = None

            persist_saidas_testes(db, db_problema)

            db.commit()
            db.refresh(db_problema)

            process_imagens_declaracoes(
                declaracoes=db_problema.declaracoes,
                declaracoes_create=problema.declaracoes,
                db=db
            )

        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Ocorreu um erro na criação do problema!"
            )

        finally:
            if os.path.exists(pacote_file_path):
                os.remove(pacote_file_path)

        return jsonable_encoder(db_problema.id)
