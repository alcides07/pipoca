from pydantic import BaseModel, Field
from typing import TypeVar, List, Generic
from schemas.common.pagination import MetadataSchema

T = TypeVar('T')


class ResponsePaginationSchema(BaseModel, Generic[T]):
    metadata: MetadataSchema = Field(
        description="Metadados acerca da resposta"
    )

    data: List[T] = Field(
        description="Lista de objetos retornados"
    )


class ResponseUnitSchema(BaseModel, Generic[T]):
    data: T = Field(
        description="Objeto retornado"
    )


class ResponseDataWithMessageSchema(BaseModel, Generic[T]):
    data: T = Field(
        description="Objeto retornado"
    )

    message: str = Field(
        description="Mensagem de feedback acerca do retorno"
    )


class ResponseMessageSchema(BaseModel):
    message: str = Field(
        description="Mensagem de feedback acerca do retorno"
    )


class ResponseValidationSchema(BaseModel):
    field: str = Field(description="Campo que possui erro")
    type: str = Field(description="Tipo do erro")
    message: str = Field(description="Mensagem de detalhamento do erro")


class ResponseValidationListSchema(BaseModel):
    errors: List[ResponseValidationSchema] = Field(
        description="Lista de erros")
