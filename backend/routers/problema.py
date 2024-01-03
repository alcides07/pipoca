from typing import Annotated
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from utils.errors import errors
from models.problema import Problema
from orm.common.index import get_all
from dependencies.authenticated_user import get_authenticated_user
from schemas.problema import ProblemaCreate, ProblemaRead
from schemas.common.pagination import PaginationSchema
from dependencies.database import get_db
from sqlalchemy.orm import Session
from orm.problema import create_problema
from schemas.common.response import ResponsePaginationSchema, ResponseUnitSchema
import zipfile
import tempfile

router = APIRouter(
    prefix="/problemas",
    tags=["problema"],
    dependencies=[Depends(get_authenticated_user)],
)


@router.get("/", response_model=ResponsePaginationSchema[ProblemaRead], summary="Lista problemas")
def read(db: Session = Depends(get_db), common: PaginationSchema = Depends()):
    problemas, metadata = get_all(db, Problema, common)

    return ResponsePaginationSchema(
        data=problemas,
        metadata=metadata
    )


@router.post("/",
             response_model=ResponseUnitSchema[ProblemaRead],
             status_code=201,
             summary="Cadastra problema",
             responses={
                 422: errors[422]
             }
             )
def create(
    problema: ProblemaCreate, db: Session = Depends(get_db)
):
    data = create_problema(db=db, problema=problema)

    return ResponseUnitSchema(data=data)


@router.post("/upload/",
             response_model=ResponseUnitSchema[ProblemaRead],
             status_code=201,
             summary="Importa problema do Polygon via pacote",
             responses={
                 422: errors[422]
             }
             )
def upload(
    pacote: Annotated[UploadFile, File(description="Pacote .zip gerado pelo Polygon")],
    db: Session = Depends(get_db),
):
    if (pacote.content_type not in ["application/zip"]):
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
        tags=[]
    )

    try:
        with zipfile.ZipFile(temp_file, 'r') as zip:
            for filename in zip.namelist():

                # Cria as tags
                if (filename.lower() == "tags"):
                    with zip.open(filename) as tags:
                        for tag in tags.readlines():
                            problema.tags.append(tag.decode().strip())

        data = create_problema(db=db, problema=problema)
        return ResponseUnitSchema(data=data)

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Erro. Ocorreu um problema no processamento do pacote!")
