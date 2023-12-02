from pydantic import BaseModel
from typing import TypeVar, List, Generic
from http import HTTPStatus

T = TypeVar('T')


class response_schema(BaseModel, Generic[T]):
    message: str | None = None
    status: HTTPStatus
    data: T | List[T] | None = None
