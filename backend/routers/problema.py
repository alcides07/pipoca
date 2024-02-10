from models.user import User
from routers.auth import oauth2_scheme
import os
import json
from fastapi import APIRouter, Body, Depends, File, HTTPException, Path, UploadFile, status
from filters.problema import ProblemaFilter, search_fields_problema
from schemas.arquivo import ArquivoCreate, SecaoEnum
from schemas.declaracao import DeclaracaoCreate
from schemas.idioma import IdiomaEnum
from schemas.problemaTeste import ProblemaTesteCreate, TipoTesteProblemaEnum
from schemas.validador import ValidadorCreate
from schemas.validadorTeste import ValidadorTesteCreate, VereditoValidadorTesteEnum
from schemas.verificador import VerificadorCreate
from schemas.verificadorTeste import VereditoVerificadorTesteEnum, VerificadorTesteCreate
from utils.bytes_to_megabytes import bytes_to_megabytes
from utils.language_parser import languages_parser
from utils.errors import errors
from models.problema import Problema
from orm.common.index import get_all, get_by_id
from dependencies.authenticated_user import get_authenticated_user
from schemas.problema import ProblemaCreate, ProblemaReadFull, ProblemaReadSimple, ProblemaUpdatePartial
from schemas.common.pagination import PaginationSchema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.problema import create_problema, update_problema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
import zipfile
import tempfile
import xml.etree.ElementTree as ET

PROBLEMA_ID_DESCRIPTION = "Identificador do problema"


router = APIRouter(
    prefix="/problemas",
    tags=["problema"],
    dependencies=[Depends(get_authenticated_user)],
)


@router.get("/", response_model=ResponsePaginationSchema[ProblemaReadSimple], summary="Lista problemas")
async def read(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    filters: ProblemaFilter = Depends(),
    token: str = Depends(oauth2_scheme)
):
    user = await get_authenticated_user(token, db)

    if (isinstance(user, User)):
        if (filters.privado == True):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            filters.privado = False

    problemas, metadata = await get_all(
        db=db,
        model=Problema,
        pagination=pagination,
        token=token,
        filters=filters,
        search_fields=search_fields_problema,
        allow_any=True
    )

    return ResponsePaginationSchema(
        data=problemas,
        metadata=metadata
    )


@router.get("/me/",
            response_model=ResponsePaginationSchema[ProblemaReadSimple],
            summary="Lista problemas pertencentes ao usuário autenticado",
            )
async def read_problemas_me(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    filters: ProblemaFilter = Depends(),
    token: str = Depends(oauth2_scheme)
):

    problemas, metadata = await get_all(
        db=db,
        model=Problema,
        pagination=pagination,
        token=token,
        filters=filters,
        search_fields=search_fields_problema,
        allow_any=True,
        me_author=True
    )

    return ResponsePaginationSchema(
        data=problemas,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitSchema[ProblemaReadFull],
            summary="Lista um problema",
            responses={
                404: errors[404]
            }
            )
async def read_id(
        id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    problema = await get_by_id(
        db=db,
        model=Problema,
        id=id,
        token=token,
        model_has_user_key=Problema
    )
    return ResponseUnitSchema(
        data=problema
    )


@router.post("/",
             response_model=ResponseUnitSchema[ProblemaReadFull],
             status_code=201,
             summary="Cadastra um problema",
             responses={
                 422: errors[422]
             }
             )
async def create(
    problema: ProblemaCreate = Body(description="Problema a ser criado"),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = await get_authenticated_user(token, db)
    data = create_problema(db=db, problema=problema, user=user)
    return ResponseUnitSchema(data=data)


@router.post("/upload/",
             response_model=ResponseUnitSchema[ProblemaReadFull],
             status_code=201,
             summary="Cadastra um problema via pacote da plataforma Polygon",
             responses={
                 422: errors[422]
             }
             )
async def upload(
    pacote: UploadFile = File(description="Pacote .zip gerado pelo Polygon"),
    privado: bool = Body(
        description="Visibilidade do problema (privado/público)"),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):

    if (pacote.content_type not in ["application/zip", "application/x-zip-compressed"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro. Formato de pacote inválido!")

    temp_file = tempfile.TemporaryFile()
    temp_file.write(pacote.file.read())
    temp_file.seek(0)

    problema = ProblemaCreate(
        nome="",
        nome_arquivo_entrada="",
        nome_arquivo_saida="",
        tempo_limite=1000,
        memoria_limite=256,
        tags=[],
        declaracoes=[],
        arquivos=[],
        verificador=VerificadorCreate(
            nome="", linguagem="", corpo="", testes=[]),
        validador=ValidadorCreate(
            nome="", linguagem="", corpo="", testes=[]),
        privado=privado,
        testes=[]
    )

    def process_files_recursos(data: ET.Element):
        for file in data.findall('.//resources/file'):
            path = file.get("path")

            if (path != None):
                with zip.open(path) as file:
                    nome = file.name.split("/")[-1]
                    corpo = file.read().decode()

                    arquivo = ArquivoCreate(
                        nome=nome, corpo=corpo, secao=SecaoEnum.RECURSO, status=None)

                    problema.arquivos.append(arquivo)

    def process_files_solucao(data: ET.Element):
        for solution in data.findall('.//solutions/solution'):
            status = str(solution.get("tag"))
            source = solution.find('source')

            if source != None:
                path = source.get("path")

            if (path != None):
                with zip.open(path) as file:
                    nome = file.name.split("/")[-1]
                    corpo = file.read().decode()

                    arquivo = ArquivoCreate(
                        nome=nome, corpo=corpo, secao=SecaoEnum.SOLUCAO, status=status)

                    problema.arquivos.append(arquivo)

    def process_tempo_limite(data: ET.Element):
        tempo_limite = data.find('.//time-limit')
        if tempo_limite != None and tempo_limite.text != None:
            problema.tempo_limite = int(tempo_limite.text)

    def process_memoria_limite(data: ET.Element):
        memoria_limite = data.find('.//memory-limit')
        if memoria_limite != None and memoria_limite.text != None:
            memoria_converted = bytes_to_megabytes(int(
                (memoria_limite.text)))

            problema.memoria_limite = memoria_converted

    def process_verificador(data: ET.Element):
        verificador = data.find('.//checker/source')
        if (verificador != None):
            path = verificador.get("path")
            linguagem = verificador.get("type")

            if path != None:
                with zip.open(path) as file:
                    nome = os.path.basename(file.name)
                    corpo = file.read().decode()

                    verificador = VerificadorCreate(
                        nome=nome, corpo=corpo, linguagem=linguagem or "", testes=[])

                    problema.verificador = verificador

    def process_validador(data: ET.Element):
        validador = data.find(".//validator/source")
        if (validador != None):
            path = validador.get("path")
            linguagem = validador.get("type")

        if path != None:
            with zip.open(path) as file:
                nome = os.path.basename(file.name)
                corpo = file.read().decode()

                validador = ValidadorCreate(
                    nome=nome, corpo=corpo, linguagem=linguagem or "", testes=[])

                problema.validador = validador

    def process_verificador_teste(data: ET.Element):
        for indice, verificador_teste in enumerate(data.findall(".//checker/testset/tests/test"), start=1):
            verdict = verificador_teste.get("verdict")
            verdict_enum = VereditoVerificadorTesteEnum(verdict)

            verificador_teste = VerificadorTesteCreate(
                numero=indice,
                veredito=verdict_enum,
                entrada=""
            )

            problema.verificador.testes.append(verificador_teste)

    def process_validador_teste(data):
        for indice, validador_teste in enumerate(data.findall(".//validator/testset/tests/test"), start=1):
            verdict = validador_teste.get("verdict")
            verdict_enum = VereditoValidadorTesteEnum(verdict)

            validador_teste = ValidadorTesteCreate(
                numero=indice,
                veredito=verdict_enum,
                entrada=""
            )

            problema.validador.testes.append(validador_teste)

    def process_name(data: ET.Element):
        if (data != None):
            problema.nome = str(data.get("short-name"))

    def process_tags(data: ET.Element):
        for tag in data.findall('.//tags/tag'):
            name = str(tag.get("value"))
            problema.tags.append(name)

    def process_tests(data: ET.Element):
        for indice, test in enumerate(data.findall(".//judging/testset/tests/test"), start=1):
            cmd = test.get("cmd")
            tipo = test.get("method")
            exemplo = test.get("sample")

            teste = ProblemaTesteCreate(
                numero=indice, tipo=TipoTesteProblemaEnum.MANUAL, exemplo=False, entrada="")

            if (cmd != None):
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

    async def process_xml(zip, filename):
        with zip.open(filename) as xml:
            content = xml.read().decode()
            data = ET.fromstring(content)

            # Atribui o tempo limite
            process_tempo_limite(data)

            # Atribui a memória limite
            process_memoria_limite(data)

            # Atribui o nome do problema
            process_name(data)

            # Atribui todos os testes do problema
            process_tests(data)

            # Atribui todas as tags
            process_tags(data)

            # Atribui todos os arquivos de recursos
            process_files_recursos(data)

            # Atribui todos os arquivos de solução
            process_files_solucao(data)

            # Atribui o verificador
            process_verificador(data)

            # Atribui os testes do verificador
            process_verificador_teste(data)

            # Atribui o validador
            process_validador(data)

            # Atribui os testes do validador
            process_validador_teste(data)

    def process_declaracoes(zip, filename):
        with zip.open(filename) as statement:
            content = statement.read().decode()
            data = json.loads(content)

            declaracao = DeclaracaoCreate(
                titulo=data["name"],
                contextualizacao=data["legend"],
                formatacao_entrada=data["input"],
                formatacao_saida=data["output"],
                tutorial=data["tutorial"],
                observacao=data["notes"],
                idioma=IdiomaEnum[languages_parser.get(
                    data["language"].capitalize(), "OT")]
            )

            problema.declaracoes.append(declaracao)

    def process_entrada_verificador_teste(zip: zipfile.ZipFile, directory: str):
        indice = 0

        for filename in zip.namelist():
            if filename != directory and filename.startswith(directory) and "." not in filename:
                with zip.open(filename) as file:
                    content = file.read().decode()
                    verificador_teste = problema.verificador.testes[indice]
                    verificador_teste.entrada = content

                    indice += 1

    def process_entrada_validador_teste(zip: zipfile.ZipFile, directory: str):
        indice = 0

        for filename in zip.namelist():
            if filename != directory and filename.startswith(directory):
                with zip.open(filename) as file:
                    content = file.read().decode()

                    validador_teste = problema.validador.testes[indice]
                    validador_teste.entrada = content

                    indice += 1

    def process_entrada_teste_manual(zip: zipfile.ZipFile, directory: str):
        indice = 0

        for filename in zip.namelist():
            if (filename != directory and filename.startswith(directory)):
                with zip.open(filename) as file:
                    content = file.read().decode()

                    teste = problema.testes[indice]
                    if (teste.tipo == TipoTesteProblemaEnum.MANUAL):
                        teste.entrada = content

                    indice += 1

    try:
        with zipfile.ZipFile(temp_file, 'r') as zip:
            for filename in zip.namelist():

                # Processa o xml global do problema
                if filename.lower() == "problem.xml":
                    await process_xml(zip, filename)

                    process_entrada_verificador_teste(
                        zip, "files/tests/checker-tests/")
                    process_entrada_validador_teste(
                        zip, "files/tests/validator-tests/")

                    process_entrada_teste_manual(
                        zip, "tests/"
                    )

                # Processa o statement de cada idioma
                if filename.startswith("statements/") and filename.endswith("problem-properties.json"):
                    process_declaracoes(zip, filename)

        user = await get_authenticated_user(token, db)
        data = create_problema(db=db, problema=problema, user=user)
        return ResponseUnitSchema(data=data)

    except HTTPException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Erro. Ocorreu uma falha no processamento do pacote!")


@router.put("/{id}/",
            response_model=ResponseUnitSchema[ProblemaReadFull],
            summary="Atualiza um problema por completo",
            responses={
                404: errors[404]
            },
            )
async def total_update(
        id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: ProblemaCreate = Body(
            description="Problema a ser atualizado por completo"),
        token: str = Depends(oauth2_scheme),
):
    user = await get_authenticated_user(token, db)
    response = await update_problema(
        db=db,
        id=id,
        problema=data,
        user=user
    )
    return ResponseUnitSchema(
        data=response
    )


@router.patch("/{id}/",
              response_model=ResponseUnitSchema[ProblemaReadFull],
              summary="Atualiza um problema parcialmente",
              responses={
                  404: errors[404]
              },
              )
async def parcial_update(
        id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: ProblemaUpdatePartial = Body(
            description="Problema a ser atualizado parcialmente"),
        token: str = Depends(oauth2_scheme),
):
    user = await get_authenticated_user(token, db)
    response = await update_problema(
        db=db,
        id=id,
        problema=data,
        user=user
    )
    return ResponseUnitSchema(
        data=response
    )
