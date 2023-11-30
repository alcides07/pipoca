from pydantic import BaseModel


class pagination_schema(BaseModel):
    q: str | None = None
    skip: int | None = None
    limit: int | None = None
