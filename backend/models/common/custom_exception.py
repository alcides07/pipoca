from pydantic import BaseModel


class Custom_Exception(Exception):
    def __init__(self, status_code: int, error: str):
        self.status_code = status_code
        self.error = error


class Custom_Exception_Schema(BaseModel):
    error: str
