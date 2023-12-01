from pydantic import BaseModel
from typing import Any
from enum import Enum
from http import HTTPStatus


class typeEnum(str, Enum):
    success = 'success'
    error = 'error'


class return_schema(BaseModel):
    type: typeEnum
    message: str
    status: HTTPStatus
    data: Any
