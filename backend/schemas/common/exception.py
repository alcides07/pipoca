from pydantic import BaseModel, Field


class ExceptionSchema(BaseModel):
    error: str = Field(description="Mensagem de erro")
