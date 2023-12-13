from pydantic import BaseModel


class Exception_Schema(BaseModel):
    error: str
