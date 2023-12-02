from pydantic import BaseModel
from typing import Any
from http import HTTPStatus


class return_schema(BaseModel):
    message: str
    status: HTTPStatus
    data: Any | None = None
