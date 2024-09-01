from constants import DIRECTION_ORDER_BY_DESCRIPTION, FIELDS_ORDER_BY_DESCRIPTION
from filters.arquivo import ArquivoFilter
from filters.problemaTeste import ProblemaTesteFilter
from routers.auth import oauth2_scheme
from fastapi import APIRouter, Body, Depends, File, HTTPException, Path, Query, UploadFile, status
from filters.problema import OrderByFieldsProblemaEnum, ProblemaFilter
from routers.user import USER_ID_DESCRIPTION
from schemas.arquivo import ArquivoReadFull
from schemas.common.compilers import CompilersEnum
from schemas.common.direction_order_by import DirectionOrderByEnum
from schemas.declaracao import DeclaracaoReadFull
from schemas.problemaResposta import ProblemaRespostaReadSimple
from schemas.problemaTeste import ProblemaTesteExecutado, ProblemaTesteReadFull
from schemas.tag import TagRead
from schemas.tarefas import TarefaIdSchema
from schemas.validador import ValidadorCreate, ValidadorReadFull
from schemas.verificador import VerificadorCreate, VerificadorReadFull
from utils.errors import errors
from dependencies.authenticated_user import get_authenticated_user
from schemas.problema import ProblemaCreate, ProblemaCreateUpload, ProblemaReadFull, ProblemaReadSimple, ProblemaIntegridade, ProblemaUpdatePartial, ProblemaUpdateTotal
from schemas.common.pagination import PaginationSchema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.problema import create_problema, create_problema_upload, get_all_problemas, get_arquivos_problema, get_declaracoes_problema, get_linguagens_problema, get_meus_problemas, get_problema_by_id, get_respostas_problema, get_integridade_problema, get_tags_problema, get_testes_exemplo_de_problema_executados, get_testes_problema, get_validador_problema, get_verificador_problema, update_problema
from schemas.common.response import ResponseListSchema, ResponsePaginationSchema, ResponseUnitRequiredSchema, ResponseUnitSchema
from enviroments import ENV


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


@router.get("/{id}/linguagens/",
            response_model=ResponseListSchema[CompilersEnum],
            summary="Lista as linguagens de programação aceitas para responder um problema",
            responses={
                404: errors[404]
            }
            )
async def read_problema_linguagens(
    db: Session = Depends(get_db),
    id: int = Path(description=PROBLEMA_ID_DESCRIPTION),
    token: str = Depends(oauth2_scheme)
):
    linguagens = await get_linguagens_problema(
        db=db,
        id=id,
        token=token
    )

    return ResponseListSchema(
        data=linguagens
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
             response_model=ResponseUnitRequiredSchema[
                 TarefaIdSchema |
                 ProblemaReadFull
             ],
             status_code=201,
             summary="Cadastra um problema via pacote da plataforma Polygon",
             responses={
                 422: errors[422]
             },
             description='''
             **A tentativa de submeter mais de uma linguagem de programação através do OPENAPI resultará em um erro de validação.** <br> <br>
             Isso ocorre devido ao OPENAPI não processar corretamente o envio de um array de opções, ao menos nesse cenário com **multipart/form-data**. <br> <br>
             O envio correto deve conter uma chave **linguagens** para cada valor desejado. <br> <br>
            '''
             )
async def upload(
    pacote: UploadFile = File(
        description="Pacote **.zip** gerado pelo Polygon"
    ),
    privado: bool = Body(
        description="Visibilidade do problema (privado/público)"),
    linguagens: list[CompilersEnum] = Body(
        description="Linguagens de programação aceitas na resolução do problema"),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):

    if (pacote.content_type not in ["application/zip", "application/x-zip-compressed"]):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Formato de pacote inválido!"
        )

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
        testes=[],
        linguagens=linguagens
    )

    problema_or_uuid = await create_problema_upload(
        db=db,
        problema=problema,
        pacote=pacote,
        token=token
    )

    if (ENV != "test"):
        return ResponseUnitRequiredSchema(
            data=TarefaIdSchema(task_uuid=problema_or_uuid)
        )

    return ResponseUnitRequiredSchema(
        data=problema_or_uuid
    )


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
