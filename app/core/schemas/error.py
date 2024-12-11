from pydantic import BaseModel


class ErrorBase(BaseModel):
    code: int
    error: str
    details: str