from pydantic import BaseModel
from typing import TypeVar, List, Generic

T = TypeVar('T')


class response_schema(BaseModel, Generic[T]):
    message: str | None = None
    data: T | List[T] | None = None
