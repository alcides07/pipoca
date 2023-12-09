from pydantic import BaseModel
from typing import Optional, TypeVar, List, Generic

T = TypeVar('T')


class Response_Schema(BaseModel, Generic[T]):
    data: T | List[T] | None = None


class Response_Message_Schema(BaseModel, Generic[T]):
    data: T | List[T] | None = None
    message: Optional[str] = None
