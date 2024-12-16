from pydantic import BaseModel

__all__ = ["ApiError"]

class ErrorBase(BaseModel):
    code: int
    error: str
    details: str

class ApiError(ErrorBase):
    pass
