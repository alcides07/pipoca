from pydantic import BaseModel, Field
from typing import TypeVar, List, Generic
from schemas.common.pagination import Metadata_Schema

T = TypeVar('T')


class Response_Pagination_Schema(BaseModel, Generic[T]):
    metadata: Metadata_Schema | None = None
    data: T | List[T] | None = None


class Response_Unit_Schema(BaseModel, Generic[T]):
    data: T | List[T] | None = None


class Response_Message_Schema(BaseModel, Generic[T]):
    data: T | List[T] | None = None
    message: str | None = None


class Response_Validation_Schema(BaseModel):
    field: str = Field(description="Campo que possui erro")
    type: str = Field(description="Tipo do erro")
    message: str = Field(description="Mensagem de detalhamento do erro")


class Response_Validation_List_Schema(BaseModel):
    errors: List[Response_Validation_Schema] = Field(
        description="Lista de erros")
