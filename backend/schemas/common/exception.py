from pydantic import BaseModel, Field


class Exception_Schema(BaseModel):
    error: str = Field(description="Mensagem de erro")
