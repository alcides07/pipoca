from pydantic import BaseModel, Field
from typing import TypeVar, List, Generic
from schemas.common.pagination import MetadataSchema

T = TypeVar('T')


class ResponsePaginationSchema(BaseModel, Generic[T]):
    metadata: MetadataSchema | None = None
    data: T | List[T] | None = None


class ResponseUnitSchema(BaseModel, Generic[T]):
    data: T | List[T] | None = None


class ResponseMessageSchema(BaseModel, Generic[T]):
    data: T | List[T] | None = None
    message: str | None = None


class Response_Validation_Schema(BaseModel):
    field: str = Field(description="Campo que possui erro")
    type: str = Field(description="Tipo do erro")
    message: str = Field(description="Mensagem de detalhamento do erro")


class Response_Validation_List_Schema(BaseModel):
    errors: List[Response_Validation_Schema] = Field(
        description="Lista de erros")
