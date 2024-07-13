from typing import Generic, TypeVar

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    error: str


R = TypeVar('R', bound=BaseModel)


class BaseQueryResponseSchema(BaseModel, Generic[R]):
    count: int
    limit: int
    offset: int
    items: R
