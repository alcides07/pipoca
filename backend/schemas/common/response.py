from pydantic import BaseModel
from typing import Optional, TypeVar, List, Generic

T = TypeVar('T')


class response_schema(BaseModel, Generic[T]):
    data: T | List[T] | None = None


class response_schema_message(BaseModel, Generic[T]):
    data: T | List[T] | None = None
    message: Optional[str] = None
