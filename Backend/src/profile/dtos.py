from pydantic import BaseModel
from typing import Optional


class UpdateUserSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


class UpdateUserResponseSchema(BaseModel):
    id: int
    name: str
    username: str
    email: str
