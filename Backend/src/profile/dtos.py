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

class UpdatePassword(BaseModel):
    current_password : str
    new_password : str
    confirm_password : str
