from pydantic import BaseModel
from typing import Optional, TypeVar, List, Generic
from schemas.common.pagination import Metadata_Schema

T = TypeVar('T')


class Response_Schema_Pagination(BaseModel, Generic[T]):
    metadata: Metadata_Schema | None = None
    data: T | List[T] | None = None


class Response_Schema_Unit(BaseModel, Generic[T]):
    data: T | List[T] | None = None


class Response_Message_Schema(BaseModel, Generic[T]):
    data: T | List[T] | None = None
    message: Optional[str] = None
