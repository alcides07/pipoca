import os
import json
import re
import zipfile
import tempfile
import xml.etree.ElementTree as ET
from constants import DIRECTION_ORDER_BY_DESCRIPTION, FIELDS_ORDER_BY_DESCRIPTION
from filters.arquivo import ArquivoFilter
from filters.problemaTeste import ProblemaTesteFilter
from routers.auth import oauth2_scheme
from fastapi import APIRouter, Body, Depends, File, HTTPException, Path, Query, UploadFile, status
from filters.problema import OrderByFieldsProblemaEnum, ProblemaFilter
from routers.user import USER_ID_DESCRIPTION
from schemas.arquivo import ArquivoCreate, ArquivoReadFull, SecaoEnum
from schemas.common.compilers import CompilersEnum
from schemas.common.direction_order_by import DirectionOrderByEnum
from schemas.declaracao import DeclaracaoCreate, DeclaracaoReadFull
from schemas.idioma import IdiomaEnum
from schemas.problemaResposta import ProblemaRespostaReadSimple
from schemas.problemaTeste import ProblemaTesteCreate, ProblemaTesteExecutado, ProblemaTesteReadFull, TipoTesteProblemaEnum
from schemas.tag import TagRead
from schemas.validador import ValidadorCreate, ValidadorReadFull
from schemas.validadorTeste import ValidadorTesteCreate, VereditoValidadorTesteEnum
from schemas.verificador import VerificadorCreate, VerificadorReadFull
from schemas.verificadorTeste import VereditoVerificadorTesteEnum, VerificadorTesteCreate
from utils.bytes_to_megabytes import bytes_to_megabytes
from utils.language_parser import languages_parser
from utils.errors import errors
from dependencies.authenticated_user import get_authenticated_user
from schemas.problema import ProblemaCreate, ProblemaCreateUpload, ProblemaReadFull, ProblemaReadSimple, ProblemaIntegridade, ProblemaUpdatePartial, ProblemaUpdateTotal
from schemas.common.pagination import PaginationSchema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.problema import create_problema, create_problema_upload, get_all_problemas, get_arquivos_problema, get_declaracoes_problema, get_meus_problemas, get_problema_by_id, get_respostas_problema, get_integridade_problema, get_tags_problema, get_testes_exemplo_de_problema_executados, get_testes_problema, get_validador_problema, get_verificador_problema, update_problema
from schemas.common.response import ResponseListSchema, ResponsePaginationSchema, ResponseUnitRequiredSchema, ResponseUnitSchema

PROBLEMA_ID_DESCRIPTION = "Identificador do problema"

router = APIRouter(
    prefix="/problemas",
    tags=["problemas"],
    dependencies=[Depends(get_authenticated_user)],
)


@router.get("/",
            response_model=ResponsePaginationSchema[ProblemaReadSimple],
            summary="Lista problemas"
            )
async def read(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    filters: ProblemaFilter = Depends(),
    token: str = Depends(oauth2_scheme),
    sort: OrderByFieldsProblemaEnum = Query(
        default=None,
        description=FIELDS_ORDER_BY_DESCRIPTION
    ),
    direction: DirectionOrderByEnum = Query(
        default=None,
        description=DIRECTION_ORDER_BY_DESCRIPTION
    )
):
    problemas, metadata = await get_all_problemas(
        db=db,
        pagination=pagination,
        token=token,
        filters=filters,
        field_order_by=sort,
        direction=direction
    )

    return ResponsePaginationSchema(
        data=problemas,
        metadata=metadata
    )


@router.get("/{id}/testes/",
            response_model=ResponsePaginationSchema[ProblemaTesteReadFull],
            summary="Lista testes pertencentes a um problema",
            responses={
                404: errors[404]
            }
            )
async def read_problema_id_testes(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    filters: ProblemaTesteFilter = Depends(),
    id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
    token: str = Depends(oauth2_scheme)
):
    testes, metadata = await get_testes_problema(
        db=db,
        id=id,
        pagination=pagination,
        filters=filters,
        token=token
    )

    return ResponsePaginationSchema(
        data=testes,
        metadata=metadata
    )


@router.get("/{id}/testesExemplosExecutados/",
            response_model=ResponseListSchema[ProblemaTesteExecutado],
            summary="Lista testes de exemplo de um problema após execução",
            responses={
                404: errors[404]
            }
            )
async def read_problema_id_testes_exemplo_executados(
    db: Session = Depends(get_db),
    id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
    token: str = Depends(oauth2_scheme)
):
    testes = await get_testes_exemplo_de_problema_executados(
        db=db,
        id=id,
        token=token
    )

    return ResponseListSchema(
        data=testes
    )


@router.get("/{id}/declaracoes/",
            response_model=ResponsePaginationSchema[DeclaracaoReadFull],
            summary="Lista declarações relacionadas a um problema",
            responses={
                404: errors[404]
            }
            )
async def read_problema_id_declaracoess(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
    token: str = Depends(oauth2_scheme)
):
    declaracoes, metadata = await get_declaracoes_problema(
        db=db,
        id=id,
        pagination=pagination,
        token=token
    )

    return ResponsePaginationSchema(
        data=declaracoes,
        metadata=metadata
    )


@router.get("/{id}/tags/",
            response_model=ResponsePaginationSchema[TagRead],
            summary="Lista tags relacionadas a um problema",
            responses={
                404: errors[404]
            }
            )
async def read_problema_id_tags(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
    token: str = Depends(oauth2_scheme)
):
    tags, metadata = await get_tags_problema(
        db=db,
        id=id,
        pagination=pagination,
        token=token
    )

    return ResponsePaginationSchema(
        data=tags,
        metadata=metadata
    )


@router.get("/usuarios/{id}/",
            response_model=ResponsePaginationSchema[ProblemaReadSimple],
            summary="Lista problemas pertencentes a um usuário",
            )
async def read_problemas_me(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    filters: ProblemaFilter = Depends(),
    token: str = Depends(oauth2_scheme),
    sort: OrderByFieldsProblemaEnum = Query(
        default=None,
        description=FIELDS_ORDER_BY_DESCRIPTION
    ),
    direction: DirectionOrderByEnum = Query(
        default=None,
        description=DIRECTION_ORDER_BY_DESCRIPTION
    ),
    id: int = Path(description=USER_ID_DESCRIPTION)
):
    problemas, metadata = await get_meus_problemas(
        db=db,
        pagination=pagination,
        token=token,
        field_order_by=sort,
        direction=direction,
        filters=filters,
        id=id
    )

    return ResponsePaginationSchema(
        data=problemas,
        metadata=metadata
    )


@router.get("/{id}/validadores/",
            response_model=ResponseUnitSchema[ValidadorReadFull],
            summary="Lista um validador pertencente a um problema",
            responses={
                404: errors[404]
            }
            )
async def read_problema_id_validador(
    db: Session = Depends(get_db),
    id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
    token: str = Depends(oauth2_scheme)
):
    validador = await get_validador_problema(
        db=db,
        id=id,
        token=token
    )

    return ResponseUnitSchema(
        data=validador
    )


@router.get("/{id}/integridade/",
            response_model=ResponseUnitRequiredSchema[ProblemaIntegridade],
            summary="Lista o status do preenchimento ou ausência das partes que compõem um problema",
            responses={
                404: errors[404]
            }
            )
async def read_problema_status(
    db: Session = Depends(get_db),
    id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
    token: str = Depends(oauth2_scheme)
):
    status = await get_integridade_problema(
        db=db,
        id=id,
        token=token
    )

    return ResponseUnitRequiredSchema(
        data=status
    )


@router.get("/{id}/verificadores/",
            response_model=ResponseUnitSchema[VerificadorReadFull],
            summary="Lista um verificador pertencente a um problema",
            responses={
                404: errors[404]
            }
            )
async def read_problema_id_verificador(
    db: Session = Depends(get_db),
    id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
    token: str = Depends(oauth2_scheme)
):
    verificador = await get_verificador_problema(
        db=db,
        id=id,
        token=token
    )

    return ResponseUnitSchema(
        data=verificador
    )


@router.get("/{id}/respostas/",
            response_model=ResponsePaginationSchema[ProblemaRespostaReadSimple],
            summary="Lista respostas pertencentes a um problema",
            responses={
                404: errors[404]
            }
            )
async def read_problema_id_respostas(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
    token: str = Depends(oauth2_scheme)
):
    respostas, metadata = await get_respostas_problema(
        db=db,
        id=id,
        pagination=pagination,
        token=token
    )

    return ResponsePaginationSchema(
        data=respostas,
        metadata=metadata
    )


@router.get("/{id}/arquivos/",
            response_model=ResponsePaginationSchema[ArquivoReadFull],
            summary="Lista arquivos pertencentes a um problema",
            responses={
                404: errors[404]
            }
            )
async def read_problema_id_arquivos(
    db: Session = Depends(get_db),
    pagination: PaginationSchema = Depends(),
    id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
    token: str = Depends(oauth2_scheme),
    filters: ArquivoFilter = Depends()
):
    arquivos, metadata = await get_arquivos_problema(
        db=db,
        id=id,
        filters=filters,
        pagination=pagination,
        token=token
    )

    return ResponsePaginationSchema(
        data=arquivos,
        metadata=metadata
    )


@router.get("/{id}/",
            response_model=ResponseUnitRequiredSchema[ProblemaReadFull],
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
    problema = await get_problema_by_id(
        db=db,
        id=id,
        token=token
    )
    return ResponseUnitRequiredSchema(
        data=problema
    )


@router.post("/",
             response_model=ResponseUnitRequiredSchema[ProblemaReadFull],
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
    data = await create_problema(
        db=db,
        problema=problema,
        token=token
    )
    return ResponseUnitRequiredSchema(data=data)


@router.post("/pacotes/",
             response_model=ResponseUnitRequiredSchema[ProblemaReadFull],
             status_code=201,
             summary="Cadastra um problema via pacote da plataforma Polygon",
             responses={
                 422: errors[422]
             }
             )
async def upload(
    pacote: UploadFile = File(
        description="Pacote **.zip** gerado pelo Polygon"
    ),
    privado: bool = Body(
        description="Visibilidade do problema (privado/público)"
    ),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):

    if (pacote.content_type not in ["application/zip", "application/x-zip-compressed"]):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Formato de pacote inválido!"
        )

    temp_file = tempfile.TemporaryFile()
    temp_file.write(pacote.file.read())
    temp_file.seek(0)

    problema = ProblemaCreateUpload(
        nome="",
        nome_arquivo_entrada="",
        nome_arquivo_saida="",
        tempo_limite=1000,
        memoria_limite=256,
        tags=[],
        declaracoes=[],
        arquivos=[],
        verificador=VerificadorCreate(
            nome="", linguagem=CompilersEnum.PYTHON_3, corpo="", testes=[]),
        validador=ValidadorCreate(
            nome="", linguagem=CompilersEnum.PYTHON_3, corpo="", testes=[]),
        privado=privado,
        testes=[]
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
                status_arquivo = str(solution.get("tag"))
                source = solution.find('source')

                if source != None:
                    path = source.get("path")
                    linguagem = source.get("type")

                if (path != None):
                    with zip.open(path) as file:
                        nome = file.name.split("/")[-1]
                        corpo = file.read().decode()
                        arquivo = ArquivoCreate(
                            nome=nome, corpo=corpo, linguagem=CompilersEnum(linguagem), secao=SecaoEnum.SOLUCAO, status=status_arquivo)

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

    async def process_xml(zip, filename):
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
                    imagens=nomes_imagens,
                    imagens_arquivos=[],
                    observacao=data["notes"],
                    idioma=IdiomaEnum[languages_parser.get(
                        data["language"].capitalize(), "OT")]
                )

                for imagem in nomes_imagens:
                    partes_filename = filename.split('/')
                    endereco_statement = '/'.join(partes_filename[:-1])
                    caminho_imagem = os.path.join(endereco_statement, imagem)

                    if (declaracao.imagens_arquivos):
                        declaracao.imagens_arquivos.append(caminho_imagem)

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

    with zipfile.ZipFile(temp_file, 'r') as zip:
        for filename in zip.namelist():

            if filename.lower() == "problem.xml":
                await process_xml(zip, filename)

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

    data = await create_problema_upload(
        db=db,
        problema=problema,
        token=token
    )

    return ResponseUnitRequiredSchema(data=data)


@router.put("/{id}/",
            response_model=ResponseUnitRequiredSchema[ProblemaReadFull],
            summary="Atualiza um problema por completo",
            responses={
                404: errors[404]
            },
            )
async def total_update(
        id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
        db: Session = Depends(get_db),
        data: ProblemaUpdateTotal = Body(
            description="Problema a ser atualizado por completo"),
        token: str = Depends(oauth2_scheme),
):
    response = await update_problema(
        db=db,
        id=id,
        problema=data,
        token=token
    )
    return ResponseUnitRequiredSchema(
        data=response
    )


@router.patch("/{id}/",
              response_model=ResponseUnitRequiredSchema[ProblemaReadFull],
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
    response = await update_problema(
        db=db,
        id=id,
        problema=data,
        token=token
    )
    return ResponseUnitRequiredSchema(
        data=response
    )
